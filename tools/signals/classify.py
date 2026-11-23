"""Rule-based relevance, geography, theme, type and organisation classification. Every decision carries its reason.

No score is published and nothing is ranked. Classification never assigns an evidence-strength label.
"""
import csv
import os
import re

import unicodedata

import yaml

from common import clean_text


class Rules:
    def __init__(self, research_dir):
        t = yaml.safe_load(open(os.path.join(research_dir, "signals", "taxonomy.yml"), encoding="utf-8"))
        c = lambda ps: [re.compile(p, re.I) for p in ps]
        self.t = t
        self.pollution = c(t["pollution_terms"])
        self.exclude = c(t["exclude_terms"]); self.exclude_always = c(t["exclude_always"]); self.instruction = c(t["instruction_like"])
        self.countries = {k: c(v["patterns"]) for k, v in t["countries"].items()}
        self.country_label = {k: v["label"] for k, v in t["countries"].items()}
        self.ambiguous = c(t["ambiguous_places"]); self.regional = c(t["regional_terms"]); self.crossborder = c(t["crossborder_terms"])
        self.out_of_scope = c(t.get("out_of_scope_places", []))
        self.themes = {k: c(v["patterns"]) for k, v in t["themes"].items()}
        self.theme_meta = t["themes"]
        self.type_rules = {k: re.compile(v, re.I) for k, v in t["type_rules"].items()}
        self.views = t["views"]; self.view_of_type = t["view_of_type"]
        self.orgs = []
        p = os.path.join(research_dir, "data", "organisations.csv")
        for o in csv.DictReader(open(p, encoding="utf-8")) if os.path.exists(p) else []:
            names = [o["organisation"]] + [a.strip() for a in (o.get("aliases") or "").split(";") if a.strip()]
            m = re.search(r"\(([A-Z][A-Za-z\-]{3,})\)", o["organisation"])
            if m: names.append(m.group(1))
            pats = []
            for n in names:
                base = re.sub(r"\s*\([^)]*\)", "", n).strip()
                for x in {n, base}:
                    if re.fullmatch(r"[A-Z][A-Z\-]{3,}", x): pats.append(re.compile(r"\b" + re.escape(x) + r"\b"))          # acronym, case-sensitive
                    elif len(x) >= 9 and " " in x: pats.append(re.compile(r"\b" + re.escape(x) + r"\b", re.I))
            if pats: self.orgs.append((o["org_id"], pats))

    def hits(self, pats, text): return sorted({p.pattern for p in pats if p.search(text or "")})

    def classify(self, item, source):
        """Return (included, reason, fields). fields carries countries, region, subjects, type, provenance, orgs, flags."""
        nf = lambda s, cap: unicodedata.normalize("NFKC", clean_text(s, cap))     # entities and markup out, PM₂.₅ -> PM2.5
        title, summary = nf(item.get("title", ""), 400), nf(item.get("summary", ""), 6000)
        both = f"{title} \n {summary}"
        req = set(source.get("requires", ["pollution", "place"]))
        flags = []
        if self.hits(self.instruction, both): flags.append("instruction-like text")
        always = self.hits(self.exclude_always, title)
        if always: return False, f"excluded: matches '{always[0]}'", {}
        pt, ps = self.hits(self.pollution, title), self.hits(self.pollution, summary)
        polluted = bool(pt) or (len(ps) >= 2 and not source.get("pollution_in_title"))
        if "pollution" in req and not polluted:
            return False, "excluded: no air-pollution term in the title (and fewer than two in the summary)", {}
        ex = self.hits(self.exclude, title)
        if ex and not pt: return False, f"excluded: '{ex[0]}' without an air-pollution term in the title", {}
        # geography
        ct = {k for k, ps_ in self.countries.items() if self.hits(ps_, title)}
        cs = {k for k, ps_ in self.countries.items() if self.hits(ps_, summary)} - ct
        named = self.hits(self.regional, both)
        regional = bool(named)
        amb = [p.pattern for p in self.ambiguous if p.search(both)]
        basis = []
        if ct: basis.append("title names " + ", ".join(self.country_label[k] for k in sorted(ct)))
        countries = set(ct)
        if cs and len(cs | ct) <= 4:
            countries |= cs; basis.append("summary names " + ", ".join(self.country_label[k] for k in sorted(cs)))
        elif cs:
            regional = True; basis.append(f"summary names {len(cs | ct)} countries in scope; treated as multi-country, not tagged one by one")
        if named: basis.append("names a region in scope (" + named[0].split("|")[0].replace("\\b", "") + ")")
        if not regional and countries and self.hits(self.crossborder, both): regional = True; basis.append("cross-border term with a country in scope")
        if amb and not countries: basis.append("ambiguous place name only (" + ", ".join(amb) + "), no country tag")
        oos = self.hits(self.out_of_scope, title)
        if oos and not ct and not self.hits(self.regional, title):
            return False, "excluded: the title names a place outside South and Southeast Asia", {}
        has_place = bool(countries) or regional
        if "place" in req and not has_place:
            return False, "excluded: no country, city or regional term in scope" + (" (ambiguous place name only)" if amb else ""), {}
        # type
        st = source["default_type"]
        if item.get("is_preprint"): st = "preprint"
        elif st not in ("news", "research"):
            for k in ("funding", "policy", "report"):
                if self.type_rules[k].search(title): st = k; break
        prov = "preprint" if item.get("is_preprint") else source["provenance_kind"]
        # topics: a title match, or at least two distinct cues for the same topic in the summary (one passing word is not a topic)
        subjects = sorted(k for k, ps_ in self.themes.items() if self.hits(ps_, title) or len(self.hits(ps_, summary)) >= 2)
        rel_int = sorted({i for s in subjects for i in self.theme_meta[s].get("related_interventions", [])})
        orgs = []
        if source.get("atlas_org_id"): orgs.append({"org_id": source["atlas_org_id"], "link_type": "publisher"})
        for oid, pats in self.orgs:
            if oid != source.get("atlas_org_id") and any(p.search(title) for p in pats): orgs.append({"org_id": oid, "link_type": "named in title"})
        reason = "included: " + ("air-pollution term in title (" + pt[0] + ")" if pt else ("two or more air-pollution terms in summary" if polluted else "source is about air quality"))
        reason += "; " + ("; ".join(basis) if basis else "regional source")
        return True, reason[:600], {"countries": sorted(countries), "country_basis": "; ".join(basis)[:300], "cross_border_region": regional,
                                    "ambiguous_places": amb, "subjects": subjects, "source_type": st, "provenance_kind": prov,
                                    "related_intervention_ids": rel_int, "organisation_ids": orgs, "content_flags": flags}
