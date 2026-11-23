"""Organisations atlas: register sources, claims and records (run once, idempotent on sources).

Run:  python3 research/analysis/add_org_atlas.py
Writes: sources.csv / claims.csv (append), organisations.csv (new columns + rows),
        projects.csv, organisation-project-roles.csv, funding-flows.csv, org-candidates.csv,
        and updates programme P16 (GEF record now read).
Every fact below was read on the page cited, on 23 November 2026, and is no later than the
22 November 2026 cutoff. Organisation-reported figures are labelled as such and never as results.
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import reg
reg.ACCESSED = "2026-11-23"
from reg import S, C
D = reg.D
CHECKED = "2026-11-23"
if any(r["claim_id"] == "C154" for r in csv.DictReader(open(reg.CLM))):
    sys.exit("Atlas claims already registered (C154 exists). Delete them first to re-run.")

CAF = "https://www.cleanairfund.org/what-we-do/our-grants/"
def cafp(n): return CAF + (f"page/{n}/" if n > 1 else "")
EPIC = "https://aqfund.epic.uchicago.edu/entities/"

# ---------- sources ----------
src = {}
def s(key, title, org, pub, date, url, typ, acc="full-text-read", lang="en", notes=""):
    src[key] = S(title, org, pub, date, url, typ, acc, lang, notes)

for n in [1, 2, 4, 6, 7, 11, 12, 13, 15, 18, 19, 20, 22, 23, 24]:
    s(f"caf{n}", f"Our grants (grant database listing, page {n})", "Clean Air Fund", "Clean Air Fund", "2026",
      cafp(n), "organisational-report", notes="Grant listing; funder's own record; amounts not shown; listing order shifts as grants are added")
s("epic_news", "EPIC Awards 39 New Projects to Improve Air Quality Monitoring and Data Access", "EPIC, University of Chicago", "EPIC Air Quality Fund",
  "2026-10-06", "https://aqfund.epic.uchicago.edu/news/epic-awards-39-new-projects-to-improve-air-quality-monitoring-and-data-access/", "organisational-report")
for k, slug_, yr in [("smart-air-bangladesh", "smart-air-bangladesh", "2026"), ("obhizatrik", "obhizatrik-foundation", "2026"),
                     ("upm", "universiti-putra-malaysia-and-go-aqs", "2026"), ("habib", "habib-university", "2026"),
                     ("thingsnode", "thingsnode", "2026"), ("ateneo", "ateneo-school-of-medicine-and-public-health-center-for-research-and-innovation", "2026"),
                     ("paqi", "pakistan-air-quality-initiative-paqi", "2025"), ("cen", "clean-energy-nepal", "2025"),
                     ("gdlabs", "green-decision-labs-and-research-pvt-ltd", "2025"), ("punjab-univ", "university-of-the-punjab", "2025"),
                     ("urban-unit", "the-urban-unit", "2025"), ("sherubtse", "sherubtse-college", "2025")]:
    s(f"epic_{k}", f"Awardee profile: {slug_.replace('-', ' ')} ({yr} awardee)", "EPIC, University of Chicago", "EPIC Air Quality Fund", yr,
      EPIC + slug_ + "/", "organisational-report", notes="Funder's awardee page; describes planned activities")
s("cun", "Breathing Easier: Protecting Children from Air Pollution (project page)", "Clean Up Nepal", "Clean Up Nepal", "2025",
  "https://www.cleanupnepal.org.np/epic", "organisational-report", notes="Listed under completed projects; outputs organisation-reported")
s("cen_shp", "Swachh Hawa Pariyojana (programme page)", "Clean Energy Nepal", "Clean Energy Nepal", "n.d.",
  "https://cen.org.np/clean-air-and-urban-mobility/swachh-hawa-pariyojana.html", "programme-description")
s("paqi_home", "Pakistan Air Quality Initiative: home page and latest briefs", "Pakistan Air Quality Initiative", "PAQI", "2026-11-21",
  "https://pakairquality.com/", "organisational-report")
s("bicara", "Bicara Udara (home page: programmes and collective impact)", "Yayasan Udara Anak Bangsa (Bicara Udara)", "Bicara Udara", "2026",
  "https://bicaraudara.id/", "organisational-report", lang="id", notes="Reach figures organisation-reported")
s("nafas_about", "About Nafas", "Nafas Indonesia", "Nafas Indonesia", "n.d.", "https://nafas.co.id/about", "organisational-report")
s("nafas_found", "Nafas Foundation (home page)", "Nafas Foundation", "Nafas Foundation", "2026", "https://nafas.foundation/", "organisational-report")
s("nafas_dbs", "Nafas Indonesia partners with DBS Foundation to expand air monitoring with 50 new sensors", "Nafas Foundation", "Nafas Indonesia",
  "2024-09-19", "https://nafas.co.id/blog/Nafas-Indonesia-partners-with-DBS-Foundation-to-expand-air-monitoring-with-50-new-sensors", "organisational-report")
s("dbs50", "Bank DBS Indonesia teams up with NAFAS to install 50 air sensors to support good air quality", "DBS", "DBS Bank", "2024-08-20",
  "https://www.dbs.com/newsroom/Bank_DBS_Indonesia_teams_up_with_NAFAS_to_install_50_air_sensors_to_support_good_air_quality", "organisational-report")
s("dbs_pneu", "Nafas Indonesia and DBS Foundation launch study on impact of air pollution and pneumonia cases in children under five in Jakarta", "DBS", "DBS Bank",
  "2025-07-10", "https://www.dbs.com/newsroom/Nafas_Indonesia_and_DBS_Foundation_launch_study_on_impact_of_air_pollution_and_pneumonia_cases_in_children_under_five_in_Jakarta",
  "organisational-report", notes="Describes a white paper; not peer reviewed")
s("airly_nafas", "Nafas – The Air Quality App Built for Jakarta (case study)", "Airly", "Airly", "n.d.",
  "https://airly.org/en/case-studies/nafas-the-air-quality-app-built-for-jakarta/", "organisational-report")
s("tcan", "About us", "Thailand Clean Air Network", "Thailand Clean Air Network", "n.d.", "https://thailandcan.net/en/about-us", "organisational-report")
s("wiki_tcab", "Clean Air Bill (Thailand)", "Wikipedia contributors", "Wikipedia", "2026", "https://en.wikipedia.org/wiki/Clean_Air_Bill_(Thailand)", "reference",
  notes="Used only for the cabinet's 2023 approval of seven drafts; cited secondary")
s("nation_house", "House passes Clean Air Bill with overwhelming 309 votes", "The Nation", "The Nation (Thailand)", "2025-10-21",
  "https://www.nationthailand.com/news/politics/40057084", "journalism")
s("nation_joint", "Thai MPs reject clean air changes for 20-member joint panel review", "The Nation", "The Nation (Thailand)", "2026-09-03",
  "https://www.nationthailand.com/news/general/40070619", "journalism")
s("prachatai_cm", "Chiang Mai haze and local governance (feature)", "Prachatai English", "Prachatai English", "2024-09-11",
  "https://prachataienglish.com/node/11115", "journalism")
s("mongabay_cm", "Citizens demand sustainable solution to haze crisis in northern Thailand", "Mongabay", "Mongabay", "2023-06",
  "https://news.mongabay.com/2023/06/citizens-demand-sustainable-solution-to-haze-crisis-in-northern-thailand", "journalism")
s("purpose_hdb", "Help Delhi Breathe: Fighting Air Pollution with Collective Action (case study)", "Purpose", "Purpose", "n.d.",
  "https://www.purpose.com/case_studies/help-delhi-breathe", "organisational-report", notes="Outcome attributions are Purpose's own and not independently verified")
s("ys_aqi", "How Delhi's AQI women ambassadors are raising awareness on air pollution in their communities", "YourStory (HerStory)", "YourStory", "2024-02",
  "https://yourstory.com/herstory/2024/02/delhi-settlements-aqi-ambassadors-air-pollution", "journalism")
s("de_wm", "Inside a Delhi 'warrior mom's' fight for clean air", "Dialogue Earth", "Dialogue Earth", "n.d.",
  "https://dialogue.earth/en/pollution/inside-a-delhi-warrior-moms-fight-for-clean-air/", "journalism")
s("respirer", "Respirer Living Sciences (home page)", "Respirer Living Sciences", "Respirer Living Sciences", "n.d.", "https://respirer.in/?p=6508", "organisational-report")
s("shakti_resp", "Impacts: Measurement and dissemination of air quality data using low-cost monitors in 10 cities", "Respirer Living Sciences / Shakti Sustainable Energy Foundation",
  "Shakti Sustainable Energy Foundation", "2021-12", "https://shaktifoundation.in/wp-content/uploads/2021/12/Impacts_Respirer.pdf", "organisational-report")
s("oizom_pr", "Oizom sets up 129 air quality monitors across 9 Smart Cities in India", "Oizom", "PR Newswire", "2022-04-20",
  "https://www.prnewswire.com/in/news-releases/oizom-sets-up-129-air-quality-monitors-across-9-smart-cities-in-india-836305727.html", "organisational-report",
  notes="Company press release")
s("airveda", "Airveda (home page: products and compliance solutions)", "Airveda", "Airveda", "n.d.", "https://www.airveda.com/", "organisational-report")
s("aurassure", "Aurassure (home page)", "Aurassure", "Aurassure", "n.d.", "https://aurassure.com/", "organisational-report")
s("cstep_set", "India's first ambient low-cost sensor evaluation facility established", "CSTEP", "CSTEP", "2026-02-24",
  "https://cstep.in/indias-first-ambient-low-cost-sensor-evaluation-facility-established/", "organisational-report")
s("cstep_pr", "Press Release: Performance Evaluation of Multi-pollutant Air Quality Sensors at Indi-SET, Bengaluru, India", "CSTEP", "CSTEP", "2026-04-23",
  "https://cstep.in/?p=328076", "evaluation")
s("cstep_annex", "Annexures: Performance Evaluation of Multipollutant Air Quality Sensors at Indi-SET Bengaluru India", "CSTEP", "CSTEP", "2026-04",
  "https://cstep.in/wp-content/uploads/2026/04/Annexures_Performance-Evaluation-of-Multipollutant-Air-Quality-Sensors-at-IndiSET-Bengaluru-India.pdf", "evaluation")
s("dh_cstep", "India's low-cost air quality sensors are not yet ready for deployment", "Deccan Herald", "Deccan Herald", "2026-04-23",
  "https://www.deccanherald.com/india/indias-low-cost-air-quality-sensors-are-not-yet-ready-for-deployment-3978685", "journalism")
s("gp_sea", "Seven Indonesia's State Officials Found Negligent for Jakarta Air Pollution", "Greenpeace Southeast Asia", "Greenpeace", "2021-09-16",
  "https://www.greenpeace.org/southeastasia/press/44679/seven-indonesias-state-officials-found-negligent-for-jakarta-air-pollution/", "organisational-report")
s("gp_kasasi", "Kasasi ditolak Mahkamah Agung, Koalisi Ibukota desak pemerintah segera laksanakan putusan pengadilan", "Greenpeace Indonesia", "Greenpeace", "2023-11",
  "https://www.greenpeace.org/indonesia/cerita/57527/kasasi-ditolak-mahkamah-agung-koalisi-ibukota-desak-pemerintah-segera-laksanakan-putusan-pengadilan/",
  "organisational-report", lang="id")
s("tbs_bela", "HC orders closure of a Jashore brick kiln", "The Business Standard", "The Business Standard", "2020-11-03",
  "https://www.tbsnews.net/bangladesh/court/hc-orders-closure-jashore-brick-kiln-153352", "journalism")
s("tbs_hrpb", "HC asks authorities to curb Dhaka's air pollution", "The Business Standard", "The Business Standard", "2019-11-26",
  "https://www.tbsnews.net/bangladesh/hc-asks-curb-dhakas-air-pollution", "journalism")
s("tbs_caps", "Dhaka had just 38 days of fresh air in six years: Study", "The Business Standard", "The Business Standard", "2022-01-27",
  "https://www.tbsnews.net/bangladesh/environment/dhaka-had-just-38-days-fresh-air-six-years-study-363217", "journalism")
s("icimod_2015", "A New Way Forward for Brick Kilns in Nepal", "ICIMOD", "ICIMOD", "2015-11-10",
  "https://icimod.org/a-new-way-forward-for-brick-kilns-in-nepal", "organisational-report")
s("icimod_2018", "Zigzag Kilns hold promise for 'greening' South Asia's brick sector", "ICIMOD", "ICIMOD", "2018-02-16",
  "https://www.icimod.org/zigzag-kilns-hold-promise-for-greening-south-asias-brick-sector/", "organisational-report")
s("livelearn", "A greener future for the schools of Hanoi", "Live & Learn", "Live & Learn", "2023-10-18", "https://livelearn.org/?p=4099", "organisational-report")
s("winrock", "Five ways USAID's Reducing Pollution project and partners collaborate for clean air in Vietnam", "Winrock International", "Winrock International",
  "2023-09-11", "https://winrock.org/five-ways-usaids-reducing-pollution-project-and-partners-collaborate-for-clean-air-in-vietnam/", "organisational-report")
s("sunstar", "DTI advances future-ready PH with UN-backed E-Mobility project", "SunStar", "SunStar Davao", "2024",
  "https://www.sunstar.com.ph/davao/dti-advances-future-ready-ph-with-un-backed-e-mobility-project", "journalism", notes="Undated in captured text; reports the 2024 project document signing")
s("gef10609", "Accelerating the adoption and scale-up of electric mobility for low-carbon city development in the Philippines (GEF ID 10609)", "Global Environment Facility",
  "GEF", "2022", "https://thegef.org/projects-operations/projects/10609", "official-dataset")
s("walk350", "Advocates walk for clean air, call for stronger action on air pollution in the Philippines", "350 Pilipinas", "350.org", "2025-12-07",
  "https://world.350.org/philippines/press-release/advocates-walk-for-clean-air-call-for-stronger-action-on-air-pollution-in-the-philippines/", "organisational-report")
s("asean_acc", "Secretary-General of ASEAN witnesses soft launching of ASEAN Coordinating Centre for Transboundary Haze Pollution Control", "ASEAN Secretariat", "ASEAN",
  "2023-09-05", "https://asean.org/secretary-general-of-asean-witnesses-soft-launching-of-asean-coordinating-centre-for-transboundary-haze-pollution-control/", "official-document")
s("crea", "About us", "Centre for Research on Energy and Clean Air", "CREA", "2026", "https://energyandcleanair.org/about/", "organisational-report")
s("openaq", "About Us", "OpenAQ", "OpenAQ", "n.d.", "https://openaq.org/about/", "organisational-report")
src["caf_hcw"] = "S050"; src["wb_rel"] = "S051"
src["wb_igp"] = "S072"; src["caf_idn"] = "S079"; src["caf_cm"] = "S080"; src["caf_wb"] = "S081"; src["mht_cs"] = "S049"
src["caf_grants"] = "S092"; src["caf_india"] = "S093"

# ---------- claims ----------
cl = {}
def c(key, section, text, keys, locator="", etype="organisational-report", geo="", period="", status="read", notes=""):
    cl[key] = C(section, text, [src[k] for k in keys], locator, etype, geo, period, status, notes)

SEC = "07"
# Funders and intermediaries
c("epic_fund", SEC, "The EPIC Air Quality Fund was launched in July 2024 with a US$1.5 million gift from Coefficient Giving and funds in-country groups over 18 months to install monitors and share data openly; it announced 39 new awardees on 6 October 2026.", ["epic_news"], "Body", geo="Global", period="2024-2026")
c("dbs_grant", SEC, "Bank DBS Indonesia announced on 20 August 2024 a partnership with Nafas to install 50 air quality sensors, as part of the grant Nafas received through the DBS Foundation Business for Impact Grant Award 2023.", ["dbs50"], "Para 1", geo="Indonesia", period="2023-2024")
# CAF grants (funder's own record)
c("caf_mht23", SEC, "Clean Air Fund's grant database lists a 2023 grant to Gujarat Mahila Housing Sewa Trust to build awareness in Delhi informal settlements and enable access to existing government protective measures.", ["caf12"], "Grant listing, 2023", geo="Delhi", period="2023")
c("caf_iitd", SEC, "Clean Air Fund lists a 2023 grant to IIT Delhi to generate localised evidence on the health and climate impacts of air pollution.", ["caf12"], "Grant listing, 2023", geo="India", period="2023")
c("caf_wri", SEC, "Clean Air Fund lists a 2023 grant to World Resources Institute to support the city administrations of Agra and Gorakhpur (Uttar Pradesh) under the 'Accelerator for Clean Air Actions' across 10 Indian cities.", ["caf12"], "Grant listing, 2023", geo="Uttar Pradesh", period="2023")
c("caf_cii", SEC, "Clean Air Fund lists grants to the Confederation of Indian Industry for the India CEO Forum for Clean Air (2019 and Phase 2 in 2023), a platform for industry leaders on air pollution.", ["caf12", "caf23"], "Grant listings, 2019 and 2023", geo="India", period="2019-2023")
c("caf_cstep", SEC, "Clean Air Fund lists a 2023 grant to CSTEP to support Punjab state authorities in developing multi-sectoral air pollution strategies aligned with the National Clean Air Programme.", ["caf12"], "Grant listing, 2023", geo="Punjab (India)", period="2023")
c("caf_teri", SEC, "Clean Air Fund lists a 2023 grant to TERI for a strategic and policy advisory unit giving technical assistance to the Uttar Pradesh Clean Air Management Programme (UP CAMP).", ["caf13"], "Grant listing, 2023", geo="Uttar Pradesh", period="2023")
c("caf_epic_in", SEC, "Clean Air Fund lists 2023 grants to EPIC-India (University of Chicago Trust) for a policy support unit for the Government of NCT of Delhi and, with the University of Warwick, a research unit supporting Delhi's Transport Department on vehicular pollution.", ["caf13"], "Grant listings, 2023", geo="Delhi", period="2023")
c("caf_cse", SEC, "Clean Air Fund lists a 2023 grant to the Centre for Science and Environment to produce a National Clean Air Programme good-practice compendium for Indian cities.", ["caf13"], "Grant listing, 2023", geo="India", period="2023")
c("caf_iitk", SEC, "Clean Air Fund lists grants to IIT Kanpur for an AI-based decision support system for Lucknow (2021), the ATMAN Centre of Excellence and a core support grant (2023).", ["caf12", "caf15", "caf18"], "Grant listings, 2021-2023", geo="Uttar Pradesh", period="2021-2023")
c("caf_icct", SEC, "Clean Air Fund lists a 2022 grant to ICCT for the TRUE Initiative in India, assessing real-world emissions of Delhi's vehicle fleet.", ["caf18"], "Grant listing, 2022", geo="Delhi", period="2022")
c("caf_2021", SEC, "Clean Air Fund lists 2021 grants in Delhi to ICLEI (city leadership with NCR urban local bodies), Pravah (youth in urban slums, Delhi and Uttar Pradesh), Clean Air Asia (MSME air pollution learnings), Sesame Workshop India (children's voices) and Swaniti (policy support for Delhi and Uttar Pradesh).", ["caf19", "caf20"], "Grant listings, 2021", geo="Delhi; Uttar Pradesh", period="2021")
c("caf_hcwh", SEC, "Clean Air Fund lists grants to Health Care Without Harm in 2019 (positioning India's health sector on air pollution) and 2023 (health professionals working with governments in Delhi, Punjab, Rajasthan and Uttar Pradesh), and names its partner programme 'Doctors For Clean Air'.", ["caf12", "caf24", "caf_hcw"], "Grant listings; case study heading", geo="India", period="2019-2023")
c("caf_jkt", SEC, "Clean Air Fund lists 2024 grants to Vital Strategies (implementing Breathe Cities in Jakarta) and C40 Cities (extended support to build Jakarta's planned Clean Air Zone).", ["caf4"], "Grant listings, 2024", geo="Jakarta", period="2024")
c("caf_airparif", SEC, "Clean Air Fund funded Airparif to run independent microsensor challenges evaluating low-cost sensors in Thailand (2023) and in India and Ghana (2024).", ["caf7", "caf11"], "Grant listings, 2023-2024", geo="Thailand; India", period="2023-2024")
c("caf_bc", SEC, "Clean Air Fund lists black-carbon research grants involving the University of Dhaka and the Maldives Climate Observatory (with Stockholm University, 2024-2027), the University of Helsinki (Himalayan mountain ecosystems in Nepal, 2025-2027) and IIT Bombay with IGSD (2025-2027).", ["caf1", "caf2"], "Grant listings", geo="Bangladesh; Maldives; Nepal; India", period="2024-2027")
c("caf_rcpch", SEC, "Clean Air Fund lists a 2024 grant to the Royal College of Paediatrics and Child Health to strengthen paediatric associations, including in Nepal, on air pollution risks to babies and children.", ["caf6"], "Grant listing, 2024", geo="Nepal", period="2024")
c("caf_ccac_in", SEC, "Clean Air Fund lists a 2020 grant to UNEP-CCAC to publish a 'State of the Air in India' assessment with the environment ministry and the Central Pollution Control Board.", ["caf22"], "Grant listing, 2020", geo="India", period="2020")
# EPIC awardees
c("epic_paqi", SEC, "EPIC's 2025 award to PAQI supports 70 affordable PM2.5 monitors installed with the National Emergencies Operation Center of Pakistan's National Disaster Management Authority, to support the National Clean Air Policy.", ["epic_paqi"], "Awardee page", geo="Pakistan", period="2025-2026")
c("epic_cen", SEC, "EPIC's 2025 award to Clean Energy Nepal supports 21 low-cost monitors in major Nepali cities with government partners, open data and youth trained to share it.", ["epic_cen"], "Awardee page", geo="Nepal", period="2025-2026")
c("epic_gdl", SEC, "EPIC's 2025 award to Green Decision Labs and Research supports 40 low-cost monitors to identify the schools in Kathmandu Valley most affected by poor air quality.", ["epic_gdlabs"], "Awardee page", geo="Kathmandu Valley", period="2025-2026")
c("epic_uu", SEC, "EPIC's 2025 award to The Urban Unit supports 160 low-cost monitors across 10 Pakistani cities with data published on an open portal and health advisories.", ["epic_urban-unit"], "Awardee page", geo="Pakistan", period="2025-2026")
c("epic_pu", SEC, "EPIC's 2025 award to the University of the Punjab supports Faisalabad's first air quality monitoring network of 10 low-cost monitors across industrial, commercial and residential areas.", ["epic_punjab-univ"], "Awardee page", geo="Faisalabad", period="2025-2026")
c("epic_sher", SEC, "EPIC's 2025 award to Sherubtse College supports low-cost PM2.5 monitors at 15 locations across Bhutan, with a counterpart in the Ministry of Energy and Natural Resources.", ["epic_sherubtse"], "Awardee page", geo="Bhutan", period="2025-2026")
c("epic_sab", SEC, "EPIC's 2026 award to Smart Air Bangladesh supports monitors around Dhaka's Matuail and Aminbazar landfills to measure the contribution of waste burning, working with BRAC Institute of Governance and Development and the Bangladesh Environmental Lawyers Association.", ["epic_smart-air-bangladesh"], "Awardee page", geo="Dhaka", period="2026-2027")
c("epic_obh", SEC, "EPIC's 2026 award to OBHIZATRIK Foundation supports 'Breathing Dhaka', placing sensors in informal settlements, industrial zones and dense residential areas and publishing readings live.", ["epic_obhizatrik"], "Awardee page", geo="Dhaka", period="2026-2027")
c("epic_habib", SEC, "EPIC's 2026 award to Habib University supports 'SindhAir', Karachi's first open continuous monitoring network in industrial zones, traffic corridors, port areas and schools, with reference monitoring in partnership with the Sindh Environmental Protection Agency.", ["epic_habib"], "Awardee page", geo="Karachi", period="2026-2027")
c("epic_tn", SEC, "EPIC's 2026 award to ThingsNode supports PM2.5 sensors along Sri Lankan transport corridors, with data made freely available to inform outdated air quality rules.", ["epic_thingsnode"], "Awardee page", geo="Sri Lanka", period="2026-2027")
c("epic_upm", SEC, "EPIC's 2026 award to Universiti Putra Malaysia and GO AQS supports 'AIRCHAMP', generating evidence to identify at-risk communities and strengthen Malaysia's Clean Air Action Plan.", ["epic_upm"], "Awardee page", geo="Malaysia", period="2026-2027")
c("epic_ateneo", SEC, "EPIC's 2026 award to the Ateneo School of Medicine and Public Health supports Cebu City's first high-density low-cost sensor network with the Cebu City Government, public health warnings and work towards a local air quality ordinance.", ["epic_ateneo"], "Awardee page", geo="Cebu City", period="2026-2027")
# Nepal
c("cun_proj", SEC, "Clean Up Nepal's 'Breathing Easier' project, funded by the EPIC Air Quality Fund with Green Decision Labs as consortium partner from 1 February 2025, reports 40 PM2.5 sensors in Kathmandu schools, open data via OpenAQ and awareness sessions for 1,500 students and 80 teachers.", ["cun"], "Project page: funding, duration, outputs", geo="Kathmandu", period="2025", notes="Outputs organisation-reported")
c("cen_shp", SEC, "Clean Energy Nepal's Swachh Hawa Pariyojana plans 12 months of community PM2.5 measurement with municipalities in 10 cities across all seven provinces, a Nepali-language dashboard and support to national and local air quality plans.", ["cen_shp"], "Programme page", "programme-description", geo="Nepal", period="n.d.")
c("kiln_np", SEC, "ICIMOD, the Federation of Nepal Brick Industries and MinErgy jointly launched a design manual for rebuilding brick kilns as improved zigzag kilns after the 2015 earthquake; ICIMOD's director general said the design could cut coal use by up to 30%.", ["icimod_2015"], "Press release", geo="Nepal", period="2015", notes="The 30% figure is a stated potential, not a measured result")
c("kiln_reg", SEC, "In February 2018 ICIMOD convened brick manufacturers from Bangladesh, India, Nepal and Pakistan in Kathmandu to exchange zigzag kiln design and construction practice.", ["icimod_2018"], "Press release", geo="South Asia", period="2018")
# Pakistan
c("paqi_id", SEC, "PAQI describes itself as an independent research organisation providing open data, scientific analysis and technical support for air quality management in Pakistan since 2016, and publishes weekly city briefs.", ["paqi_home"], "Home page", geo="Pakistan", period="2016-2026")
c("paqi_burn", SEC, "PAQI's November 2026 crop-burning report found Lahore averaged 175 µg/m³ of PM2.5 on days its air had passed over active burning, against 93 µg/m³ on other days.", ["paqi_home"], "Latest reports, 9 Nov 2026", "primary-study", geo="Lahore", period="2026")
# Bangladesh
c("bela_kiln", SEC, "In November 2020 the High Court declared a Jashore brick kiln's operations illegal and ordered it shut, disposing of a writ petition filed by the Bangladesh Environmental Lawyers Association.", ["tbs_bela"], "Para 1-2", "journalism", geo="Jashore", period="2020")
c("hrpb", SEC, "Human Rights and Peace for Bangladesh filed a writ on Dhaka's air pollution in January 2019; the High Court ordered the Department of Environment to run mobile court drives twice a week against polluters.", ["tbs_hrpb"], "Body", "journalism", geo="Dhaka", period="2019")
c("caps", SEC, "Stamford University's Center for Atmospheric Pollution Studies (CAPS) reported that Dhaka had acceptable air on only 38 days between 2016 and 2021.", ["tbs_caps"], "Para 1", "journalism", geo="Dhaka", period="2016-2021")
# India
c("hdb_purpose", SEC, "Purpose reports that it worked with the IKEA Foundation and Clean Air Fund to develop Help Delhi Breathe, a coalition campaign begun in 2015, and gave an innovation micro-grant for its first materials.", ["purpose_hdb"], "Case study", geo="Delhi", period="2015-", notes="Outcomes listed on the page are Purpose's attributions, not shown here")
c("hdb_aqi", SEC, "Mahila Housing Trust and Help Delhi Breathe train women from Delhi's unrecognised settlements as 'AQI ambassadors' who carry portable monitors; Help Delhi Breathe also works with Bucketlist and the Centre for Social Equity and Inclusion on door-to-door drives.", ["ys_aqi"], "Body", "journalism", geo="Delhi", period="2024")
c("wm", SEC, "Warrior Moms, co-founded in 2020 by Bhavreen Kandhari, is a network of mothers across India campaigning for clean air and climate action for their children.", ["de_wm"], "Body", "journalism", geo="India", period="2020-")
c("respirer", SEC, "From December 2017 Respirer Living Sciences, IIT Kanpur and Shakti Sustainable Energy Foundation built a sensor-based PM2.5 and PM10 network across 10 Indian cities using Respirer's Atmos devices.", ["shakti_resp"], "Executive summary", geo="India", period="2017-2021")
c("oizom", SEC, "Oizom, an Ahmedabad-based monitoring company, announced in April 2022 that it had set up 129 air quality monitors across nine Indian smart cities, including Bhagalpur in Bihar.", ["oizom_pr"], "Press release", geo="India", period="2022", notes="Company-reported")
c("airveda", SEC, "Airveda states that it is an approved vendor for construction-site air quality monitoring to the Delhi Pollution Control Committee and several Maharashtra municipal corporations, where rules require sites to monitor and share data.", ["airveda"], "Home page, 'Clean Construction'", geo="Delhi; Maharashtra", period="2026", notes="Company-reported")
c("aurassure", SEC, "Aurassure markets environmental and air quality monitoring for cities and renewable-energy sites.", ["aurassure"], "Home page", geo="India", period="2026", notes="Company-reported")
c("indiset", SEC, "CSTEP set up the India Sensor Evaluation and Training (Indi-SET) facility in Bengaluru in December 2023 for independent testing, calibration and training on low-cost sensors.", ["cstep_set"], "Body", geo="Bengaluru", period="2023-2026")
c("indiset_eval", SEC, "CSTEP's April 2026 evaluation co-located 48 multi-pollutant sensor devices from six manufacturers (Aeron, Airveda, Airvoice, Aurassure, Respirer, Sensit) with a reference monitor for up to eight months; none of the manufacturers met precision targets for nitrogen dioxide and ozone.", ["cstep_pr", "cstep_annex", "dh_cstep"], "Press release; annexure contents; news report", "evaluation", geo="Bengaluru", period="2025-2026")
# Indonesia
c("bicara", SEC, "Bicara Udara is a non-profit that advocates for clean-air policy, running an ambassadors programme (Biru Voices), a discussion platform (Biru Talks) and a schools alliance (Biru School Alliance).", ["bicara"], "Home page", geo="Indonesia", period="2026")
c("nafas_co", SEC, "Nafas Indonesia states that it operates the largest air quality sensor network in Greater Jakarta, with more than 100 outdoor sensors built with the European sensor company Airly and calibrated against local reference stations.", ["nafas_about", "airly_nafas"], "About page; supplier case study", geo="Jabodetabek", period="2026", notes="Company-reported")
c("nafas_fd", SEC, "Nafas Foundation describes itself as a non-profit initiative of Nafas Indonesia, and says the network has grown to more than 219 sensors across 23 cities and is now 'powered by the Nafas Foundation'.", ["nafas_found"], "Home page", geo="Indonesia", period="2026", notes="Organisation-reported")
c("nafas_dbs", SEC, "Nafas reported in September 2024 that it had installed 19 of the 50 DBS Foundation-supported sensors across 14 Indonesian cities.", ["nafas_dbs"], "Blog", geo="Indonesia", period="2024", notes="Organisation-reported")
c("nafas_pneu", SEC, "A July 2025 white paper by Nafas, DBS Foundation and the University of Indonesia's Faculty of Public Health reports that a 10 µg/m³ rise in PM2.5 was associated with a twofold rise in pneumonia prevalence among under-fives in several Jakarta sub-districts.", ["dbs_pneu"], "Key findings", "organisational-report", geo="Jakarta", period="2023", notes="White paper; association only; not peer reviewed")
c("jkt_suit", SEC, "On 16 September 2021 the Central Jakarta District Court ruled for the Citizens' Lawsuit on Jakarta Air Pollution, finding seven state officials negligent, including the President and three governors.", ["gp_sea"], "Para 1-2", geo="Jakarta", period="2021")
c("jkt_kasasi", SEC, "On 13 November 2023 the Supreme Court rejected the government's cassation appeal; Koalisi Ibukota, the citizens' coalition behind the lawsuit, urged the government to implement the ruling.", ["gp_kasasi"], "Body", geo="Jakarta", period="2023", notes="Implementation of the ruling not established in sources read")
# Thailand
c("tcan", SEC, "Thailand Clean Air Network describes itself as a group of citizen volunteers and academics working with public, private and civil-society actors for clean air in Thailand.", ["tcan"], "About page", geo="Thailand", period="n.d.")
c("tcan_bill", SEC, "One of seven Clean Air Act drafts approved by Thailand's cabinet on 28 November 2023 was proposed by Thailand Clean Air Network.", ["wiki_tcab"], "House of Representatives section", "reference", geo="Thailand", period="2023")
c("th_bill", SEC, "Thailand's House passed the Clean Air Bill 309-0 on 21 October 2025; in September 2026 the House rejected the Senate's amendments 414-2, sending the bill to a 20-member joint committee. No source read shows it enacted by the cutoff.", ["nation_house", "nation_joint"], "News reports", "journalism", geo="Thailand", period="2025-2026")
c("cmbc", SEC, "The Chiang Mai Breath Council was established in 2019 by public-health, private-sector and civil-society organisations as a mechanism for tackling Chiang Mai's air pollution.", ["prachatai_cm"], "Fire management section", "journalism", geo="Chiang Mai", period="2019-2024")
c("cm_suit", SEC, "More than 1,700 plaintiffs filed a lawsuit at the Chiang Mai Administrative Court on 10 April 2023 against the Prime Minister and national bodies for failing to address seasonal haze.", ["mongabay_cm"], "Body", "journalism", geo="Chiang Mai", period="2023")
# Viet Nam
c("ll_green", SEC, "Live & Learn Vietnam reports that its Building Green Schools for a Green Hanoi programme, piloted in 2021, involved more than 69 schools in four districts and scaled to all 93 schools in Dong Anh district, supported by the USAID-funded CAfCA project with Hanoi's environment and education departments.", ["livelearn"], "Story", geo="Hanoi", period="2021-2023", notes="Organisation-reported; no air-quality outcome reported")
c("winrock", SEC, "Winrock International led the USAID Reducing Pollution project in Viet Nam, working on open burning of waste and straw, craft-village emissions (including aluminium recycling at Binh Yen with VESDI) and a roadmap for vehicle emission regulations.", ["winrock"], "Article", geo="Northern Viet Nam", period="2023")
# Philippines
c("gef_emob", SEC, "The GEF records project 10609 (e-mobility in the Philippines) with UNIDO as implementing agency and the Department of Trade and Industry as executing agency, approved for implementation on 1 July 2022 with a GEF grant of US$3,788,990 and US$77,477,969 of co-financing.", ["gef10609"], "Project details; financials", "official-dataset", geo="Philippines", period="2022-")
c("emob_cons", SEC, "UNIDO enlisted a consortium of Clean Air Asia, De La Salle University, the Electric Vehicle Association of the Philippines and the Urban Electric Mobility Initiative for E-Mobility ASAP, which focuses on electric public utility vehicles, electric two-wheelers, batteries and electronics.", ["sunstar"], "Body", "journalism", geo="Philippines", period="2024-2027")
c("walk", SEC, "Health Care Without Harm Southeast Asia and 350 Pilipinas organised a Walk for Clean Air in Quezon City on 7 December 2025 with more than 500 participants, calling for updated air quality standards.", ["walk350"], "Para 1", geo="Quezon City", period="2025")
# Regional
c("acc", SEC, "The ASEAN Coordinating Centre for Transboundary Haze Pollution Control was soft-launched on 5 September 2023 at the 43rd ASEAN Summit hosted by Indonesia.", ["asean_acc"], "News item", "official-document", geo="ASEAN", period="2023")
c("crea", SEC, "CREA is an independent research organisation registered as a non-profit in Finland, with staff across Asia and Europe, funded by philanthropic grants and commissioned research.", ["crea"], "About page", geo="Regional", period="2026")
c("openaq", SEC, "OpenAQ is a non-profit that aggregates and harmonises open air quality data on an open-access platform.", ["openaq"], "About page", geo="Global", period="n.d.")

# ---------- organisations ----------
NEW_COLS = ["slug", "category", "primary_type", "legal_form", "profit_status", "hq_country", "countries_active", "places",
            "domains", "communities", "system_roles", "summary", "why_it_matters", "website", "record_status",
            "activity_period", "last_public_activity", "date_last_checked", "source_class", "business_role",
            "independent_test", "conflict_note", "funder_id", "aliases", "claim_ids", "record_origin"]
def O(org_id, name, category, primary_type, summary, why, claims, sources_, *, sector="", functions="", legal="Not established from sources read",
      profit="nonprofit", hq="", countries="", places="", domains="", communities="", roles="", website="", status="active at cutoff",
      period="", last="", sclass="organisation-reported", brole="", itest="", conflict="", funder_id="", aliases="", programme="",
      activity="", outputs="", outcomes="No adequate evidence found", quality="", gaps="", partners="", funding=""):
    return dict(org_id=org_id, organisation=name, sector=sector or primary_type, functions=functions, programme_or_role=programme,
                location=places, communities_served=communities, specific_activity_verified=activity or summary,
                status_at_cutoff=status, partners=partners, funding_where_public=funding, outputs=outputs,
                demonstrated_outcomes=outcomes, evidence_quality=quality or sclass, gaps=gaps,
                source_ids=";".join(src[k] for k in sources_), slug=org_id, category=category, primary_type=primary_type,
                legal_form=legal, profit_status=profit, hq_country=hq, countries_active=countries, places=places, domains=domains,
                communities=communities, system_roles=roles, summary=summary, why_it_matters=why, website=website,
                record_status=status, activity_period=period, last_public_activity=last, date_last_checked=CHECKED,
                source_class=sclass, business_role=brole, independent_test=itest, conflict_note=conflict, funder_id=funder_id,
                aliases=aliases, claim_ids=";".join(cl[k] for k in claims), record_origin="atlas 2026-11-23")

NEW = [
 # ---- funders / intermediaries
 O("epic-aq-fund", "EPIC Air Quality Fund (University of Chicago)", "funder", "Philanthropic fund (university-hosted regranter)",
   "Gives 18-month grants to local groups in countries with little public air data to install monitors and publish the readings openly.",
   "Many of South Asia's newest open monitoring networks outside capital cities are paid for by this fund.",
   ["epic_fund"], ["epic_news"], functions="financing; grantmaking", hq="global", countries="nepal;pakistan;bangladesh;bhutan;sri-lanka;malaysia;philippines",
   domains="ambient monitoring; data systems", roles="evidence", website="https://aqfund.epic.uchicago.edu/", period="2024-", last="2026-10-06",
   sclass="funder-reported", legal="Programme of the Energy Policy Institute at the University of Chicago", aliases="EPIC AQ Fund",
   outcomes="Funder reports policy influence by some awardees; not independently evaluated"),
 O("coefficient-giving", "Coefficient Giving", "funder", "Philanthropic funder",
   "Gave the US$1.5 million gift that launched the EPIC Air Quality Fund in July 2024.",
   "Shows how one philanthropic gift can seed many small monitoring grants.", ["epic_fund"], ["epic_news"],
   functions="financing; grantmaking", hq="global", countries="", domains="ambient monitoring", roles="evidence", sclass="funder-reported",
   period="2024", last="2024-07", conflict="Any link to the 'Open Philanthropy' research-queue entry in funders.csv is not verified here"),
 O("dbs-foundation", "DBS Foundation", "funder", "Corporate foundation (bank)",
   "Gave Nafas a 2023 Business for Impact grant that paid for 50 new air sensors in Indonesian cities.",
   "An example of corporate philanthropy paying for public-facing monitoring run by a company.",
   ["dbs_grant", "nafas_pneu"], ["dbs50", "dbs_pneu"], functions="financing; grantmaking", hq="singapore", countries="indonesia",
   domains="ambient monitoring", roles="evidence", sclass="funder-reported", period="2023-2025", last="2025-07-10", profit="corporate foundation",
   conflict="Bank DBS Indonesia also hosts sensors at its own sites and publicises the partnership"),
 # ---- India
 O("help-delhi-breathe", "Help Delhi Breathe", "community", "Citizen campaign coalition",
   "A Delhi campaign coalition that trains women from unrecognised settlements, with Mahila Housing Trust, to measure air quality and share information.",
   "Brings people who are rarely heard into Delhi's clean-air debate.", ["hdb_purpose", "hdb_aqi", "caf_mht23"], ["purpose_hdb", "ys_aqi", "mht_cs"],
   functions="organising; advocacy", hq="india", countries="india", places="Delhi (Gokulpuri, Bhalaswa, Nandnagri, Bakkarwala)",
   domains="community-led monitoring; outdoor workers", communities="Women in unrecognised settlements; women construction workers",
   roles="reduce-exposure; accountability", period="2015-", last="2024-02", sclass="journalism and funder accounts",
   partners="Mahila Housing Trust; Bucketlist; Centre for Social Equity and Inclusion", outcomes="No adequate evidence found (no measured exposure or policy outcome reported)"),
 O("warrior-moms", "Warrior Moms", "community", "Parents' network",
   "A network of mothers across India, started in 2020, that campaigns for clean air for children and presses authorities to act.",
   "Parents are a large, motivated constituency that officials hear.", ["wm"], ["de_wm"], functions="advocacy; organising",
   hq="india", countries="india", places="Delhi and other states", domains="schools and childcare; rights and legal enforcement",
   communities="Children and parents", roles="accountability", period="2020-", sclass="journalism", legal="Informal network (as described)"),
 O("dfcca", "Doctors for Clean Air (Health Care Without Harm programme)", "network", "Health professionals' network",
   "A network of doctors, run with Health Care Without Harm, that speaks to governments and the public about the health effects of air pollution.",
   "Doctors are trusted messengers on health harm.", ["caf_hcwh"], ["caf_hcw", "caf12", "caf24"], functions="advocacy; capacity building",
   hq="india", countries="india", places="Delhi, Punjab, Rajasthan, Uttar Pradesh", domains="health facilities; respiratory care",
   communities="Patients; health workers", roles="protect-health; accountability", sclass="funder-reported", period="2019-",
   aliases="Doctors for Clean Air and Climate Action; DFCA"),
 O("cstep", "Center for Study of Science, Technology and Policy (CSTEP)", "research", "Research institute (think tank)",
   "Runs India's first independent test bed for low-cost air sensors and advises state governments on clean-air plans.",
   "Its tests show which sensor readings can be trusted before cities buy them.", ["indiset", "indiset_eval", "caf_cstep"],
   ["cstep_set", "cstep_pr", "cstep_annex", "caf12"], functions="research; evaluation; technical assistance", hq="india", countries="india",
   places="Bengaluru; Punjab", domains="ambient monitoring; data systems", roles="evidence; accountability", website="https://cstep.in/",
   period="2023-", last="2026-04-23", sclass="independent evaluation", outcomes="Independent sensor test published (2026)"),
 O("epic-india", "EPIC-India (University of Chicago Trust)", "research", "Research and policy unit",
   "Ran Clean Air Fund-supported policy and transport research units advising the Delhi government on clean-air targets and vehicle pollution.",
   "Embeds researchers alongside the officials who make decisions.", ["caf_epic_in"], ["caf13"], functions="research; technical assistance",
   hq="india", countries="india", places="Delhi", domains="transport/freight/e-mobility", roles="evidence", sclass="funder-reported", period="2023-", last="2023"),
 O("icct", "International Council on Clean Transportation (ICCT)", "research", "International research organisation",
   "Measured the real-world emissions of Delhi's vehicles to inform transport policy (TRUE Initiative, funded 2022).",
   "Real-world tests reveal emissions that lab tests miss.", ["caf_icct"], ["caf18"], functions="research", hq="global", countries="india",
   places="Delhi", domains="transport/freight/e-mobility", roles="evidence", sclass="funder-reported", period="2022", last="2022", status="historical"),
 O("iclei-south-asia", "ICLEI", "network", "Local-government network",
   "Worked with urban local bodies in Delhi-NCR to build capacity to carry out city clean-air action plans (2021 grant).",
   "City bodies hold many of the levers but often lack staff.", ["caf_2021"], ["caf19"], functions="technical assistance", hq="global",
   countries="india", places="Delhi-NCR", domains="data systems", roles="accountability", sclass="funder-reported", period="2021", status="historical"),
 O("pravah", "Pravah", "ngo", "Youth NGO", "Developed young people's skills to drive clean-air action in urban slums of Delhi and Uttar Pradesh (2021 grant).",
   "Young people in low-income areas are both exposed and rarely consulted.", ["caf_2021"], ["caf19"], functions="organising", hq="india",
   countries="india", places="Delhi; Uttar Pradesh", domains="community mobilisation", communities="Young people in urban slums",
   roles="accountability", sclass="funder-reported", period="2021", status="historical"),
 O("sesame-india", "Sesame Workshop India", "ngo", "Children's media NGO", "Brought children's voices into Delhi's air pollution debate ('Mera Planet, Mera Ghar', 2021 grant).",
   "Children are among the most affected and least heard.", ["caf_2021"], ["caf20"], functions="public communication", hq="india", countries="india",
   places="Delhi", domains="schools and childcare", communities="Children", roles="accountability", sclass="funder-reported", period="2021", status="historical"),
 O("swaniti", "Swaniti", "ngo", "Policy support NGO", "Gave policy and communication support to policymakers in Delhi and Uttar Pradesh on air quality (2021 grant).",
   "Helps elected officials act on evidence.", ["caf_2021"], ["caf20"], functions="technical assistance", hq="india", countries="india",
   places="Delhi; Uttar Pradesh", domains="data systems", roles="accountability", sclass="funder-reported", period="2021", status="historical"),
 O("iit-delhi", "IIT Delhi", "research", "Academic institution", "Generates local evidence on the health and climate effects of air pollution (2023 Clean Air Fund grant).",
   "Local evidence carries more weight with Indian policymakers.", ["caf_iitd"], ["caf12"], functions="research", profit="public",
   hq="india", countries="india", domains="health facilities", roles="evidence", sclass="funder-reported", period="2023"),
 O("cii", "Confederation of Indian Industry (CII)", "private", "Industry association",
   "Runs the India CEO Forum for Clean Air, a platform for company leaders on air pollution, funded in two phases by Clean Air Fund.",
   "Industry is both a source of pollution and a source of solutions; commitments need checking against delivery.", ["caf_cii"], ["caf12", "caf23"],
   functions="advocacy", profit="business association", hq="india", countries="india", domains="industrial emissions", roles="reduce-emissions",
   sclass="funder-reported", brole="C: association of regulated emitters and suppliers", period="2019-2023",
   conflict="Members include emitters; no delivered emission reductions reported in sources read"),
 O("respirer", "Respirer Living Sciences", "private", "Company: air-sensor maker and data services",
   "Makes the Atmos low-cost air sensor; built a 10-city monitoring network with IIT Kanpur and Shakti Foundation from 2017.",
   "Its devices are widely used, and were among those tested independently by CSTEP in 2026.", ["respirer", "indiset_eval"],
   ["shakti_resp", "respirer", "cstep_annex"], functions="technology supply; installation; operations and maintenance", profit="for-profit",
   legal="Private company", hq="india", countries="india", domains="ambient monitoring", roles="evidence", website="https://respirer.in/",
   period="2017-", sclass="company-reported; independent test", brole="A: solution provider",
   itest="Included in CSTEP Indi-SET evaluation (2026): no manufacturer met NO2 and O3 precision targets", outcomes="Activity documented; outcome not independently evaluated",
   conflict="Sells devices to the governments and funders that use its data"),
 O("airveda", "Airveda", "private", "Company: air-sensor maker", "Sells air quality monitors and data, including for construction sites that rules require to monitor dust and report to regulators.",
   "Shows how regulation creates a market for monitoring; data quality then matters for enforcement.", ["airveda", "indiset_eval"], ["airveda", "cstep_annex"],
   functions="technology supply; installation", profit="for-profit", legal="Private company", hq="india", countries="india", places="Delhi; Mumbai; Pune; Thane",
   domains="construction dust; ambient monitoring", roles="evidence", website="https://www.airveda.com/", sclass="company-reported; independent test",
   brole="A: solution provider in a compliance market", itest="Included in CSTEP Indi-SET evaluation (2026)", outcomes="Activity documented; outcome not independently evaluated"),
 O("aurassure", "Aurassure", "private", "Company: environmental monitoring", "Sells environmental and air quality monitoring for cities and renewable-energy sites.",
   "One of six manufacturers whose sensors CSTEP tested in 2026.", ["aurassure", "indiset_eval"], ["aurassure", "cstep_annex"],
   functions="technology supply", profit="for-profit", legal="Private company", hq="india", countries="india", places="Bengaluru",
   domains="ambient monitoring", roles="evidence", website="https://aurassure.com/", sclass="company-reported; independent test",
   brole="A: solution provider", itest="Included in CSTEP Indi-SET evaluation (2026)", outcomes="Activity documented; outcome not independently evaluated"),
 O("oizom", "Oizom", "private", "Company: air-monitoring equipment", "An Ahmedabad company that says it has installed 129 air monitors across nine Indian smart cities.",
   "Smart-city budgets buy many monitors; what decisions follow is rarely reported.", ["oizom"], ["oizom_pr"], functions="technology supply; installation",
   profit="for-profit", legal="Private company", hq="india", countries="india", places="Nine smart cities including Bhagalpur", domains="ambient monitoring",
   roles="evidence", sclass="company-reported", brole="A: solution provider", itest="No independent performance test found in sources read",
   period="2022", last="2022-04-20", outcomes="Activity documented; outcome not independently evaluated"),
 O("shakti-foundation", "Shakti Sustainable Energy Foundation", "funder", "Philanthropic foundation",
   "Funded a 10-city low-cost sensor network built by Respirer Living Sciences and IIT Kanpur from 2017.",
   "An early Indian funder of affordable monitoring.", ["respirer"], ["shakti_resp"], functions="financing", hq="india", countries="india",
   domains="ambient monitoring", roles="evidence", sclass="funder-reported", period="2017-2021", status="historical"),
 O("purpose", "Purpose", "ngo", "Campaign agency", "Helped create the Help Delhi Breathe campaign with the IKEA Foundation and Clean Air Fund and gave it a micro-grant.",
   "Campaign design shapes who gets mobilised.", ["hdb_purpose"], ["purpose_hdb"], functions="public communication; financing", hq="global",
   countries="india", places="Delhi", domains="community mobilisation", roles="accountability", sclass="organisation-reported", period="2015-", status="historical"),
 O("airparif", "Airparif", "research", "Air quality agency (France)", "Ran Clean Air Fund-supported microsensor challenges that independently compared low-cost sensors in Thailand (2023) and India (2024).",
   "Independent comparisons protect buyers from overstated sensor claims.", ["caf_airparif"], ["caf7", "caf11"], functions="evaluation",
   hq="global", countries="thailand;india", domains="ambient monitoring", roles="evidence", sclass="funder-reported", period="2023-2024"),
 O("iit-bombay", "IIT Bombay", "research", "Academic institution", "Studies black and brown carbon with IGSD using Indian measurements (2025-2027 Clean Air Fund grant).",
   "Black carbon links air quality and climate.", ["caf_bc"], ["caf2"], functions="research", profit="public", hq="india", countries="india",
   domains="source apportionment", roles="evidence", sclass="funder-reported", period="2025-2027"),
 # ---- Nepal
 O("clean-energy-nepal", "Clean Energy Nepal", "ngo", "National NGO", "Sets up low-cost PM2.5 monitors with municipalities across Nepal's provinces and publishes the data in Nepali.",
   "Most of Nepal outside Kathmandu has no working public monitor.", ["cen_shp", "epic_cen"], ["cen_shp", "epic_cen"],
   functions="monitoring; advocacy; technical assistance", hq="nepal", countries="nepal", places="10 cities including provincial capitals",
   domains="ambient monitoring; data systems", communities="Urban residents; youth", roles="evidence; accountability",
   website="https://cen.org.np/", period="2025-", outcomes="Measurement only; no exposure or policy outcome reported yet"),
 O("clean-up-nepal", "Clean Up Nepal", "ngo", "National NGO", "Measured PM2.5 in Kathmandu schools with 40 sensors and ran awareness sessions for students and teachers (EPIC-funded, from 2025).",
   "Parents and schools can see how polluted classrooms and playgrounds are.", ["cun_proj"], ["cun"], functions="monitoring; public communication; advocacy",
   hq="nepal", countries="nepal", places="Kathmandu", domains="schools and childcare; ambient monitoring", communities="Schoolchildren; teachers",
   roles="evidence", website="https://www.cleanupnepal.org.np/", period="2025", status="completed project (listed under completed projects)",
   outputs="40 sensors; 1,500 students and 80 teachers reached (organisation-reported)", outcomes="No adequate evidence found (measurement is not exposure reduction)"),
 O("gd-labs", "Green Decision Labs and Research", "private", "Company: environmental research", "Installs low-cost monitors to find which Kathmandu Valley schools have the worst air (EPIC 2025 award).",
   "Targets attention to the most exposed children.", ["epic_gdl", "cun_proj"], ["epic_gdlabs", "cun"], functions="monitoring; research", profit="for-profit",
   legal="Private limited company (Pvt. Ltd., per EPIC page)", hq="nepal", countries="nepal", places="Kathmandu Valley", domains="schools and childcare; ambient monitoring",
   communities="Schoolchildren", roles="evidence", period="2025-", sclass="funder-reported", brole="A: research and data services"),
 O("icimod", "ICIMOD", "research", "Intergovernmental research centre", "Co-developed improved zigzag brick-kiln designs with Nepal's brick industry and convened kiln owners across South Asia.",
   "Brick kilns are a major regional source of black carbon.", ["kiln_np", "kiln_reg"], ["icimod_2015", "icimod_2018"], functions="research; technical assistance",
   profit="intergovernmental", hq="nepal", countries="nepal;india;bangladesh;pakistan", domains="brick kilns", roles="reduce-emissions; evidence",
   website="https://www.icimod.org/", period="2015-2018", aliases="International Centre for Integrated Mountain Development"),
 O("fnbi", "Federation of Nepal Brick Industries", "private", "Industry association", "Co-launched a kiln design manual with ICIMOD and MinErgy to help owners rebuild cleaner zigzag kilns after the 2015 earthquake.",
   "Kiln owners decide whether cleaner designs are actually built.", ["kiln_np"], ["icimod_2015"], functions="technical assistance", profit="business association",
   hq="nepal", countries="nepal", domains="brick kilns", roles="reduce-emissions", brole="B/C: association of regulated emitters adopting cleaner practice",
   period="2015", status="historical", sclass="partner-reported", outcomes="No measured emission reduction across members found"),
 O("minergy", "MinErgy", "private", "Technical service provider", "Co-authored the zigzag kiln design manual for Nepal with ICIMOD and the brick federation.",
   "Supplies the engineering behind cleaner kilns.", ["kiln_np"], ["icimod_2015"], functions="technical assistance; technology supply", profit="unclear",
   hq="nepal", countries="nepal", domains="brick kilns", roles="reduce-emissions", brole="A: solution provider", period="2015", status="historical",
   sclass="partner-reported", legal="Not confirmed from a primary source (CCAC partner page blocked automated access)"),
 # ---- Pakistan
 O("paqi", "Pakistan Air Quality Initiative (PAQI)", "research", "Independent research organisation", "Publishes open air quality data and weekly city briefs for Pakistan, and is adding 70 monitors with the national disaster agency.",
   "In much of Pakistan there is no routine public measurement.", ["paqi_id", "paqi_burn", "epic_paqi"], ["paqi_home", "epic_paqi"],
   functions="monitoring; research; technical assistance", hq="pakistan", countries="pakistan", places="Lahore; Karachi; Multan; Islamabad; national",
   domains="ambient monitoring; crop residue and agriculture", roles="evidence; accountability", website="https://pakairquality.com/", period="2016-", last="2026-11-21",
   outcomes="Measurement and analysis; no policy outcome attributed in sources read"),
 O("urban-unit", "The Urban Unit (Punjab)", "public", "Public-sector company (Punjab)", "Installing 160 low-cost monitors across 10 Pakistani cities with an open data portal and health advisories (EPIC 2025 award).",
   "Ties monitoring to a public body that can issue advisories.", ["epic_uu"], ["epic_urban-unit"], functions="monitoring; data systems", profit="public",
   hq="pakistan", countries="pakistan", places="10 cities", domains="ambient monitoring; data systems", roles="evidence", sclass="funder-reported", period="2025-"),
 O("university-of-the-punjab", "University of the Punjab", "research", "Academic institution", "Building Faisalabad's first air monitoring network of 10 low-cost monitors (EPIC 2025 award).",
   "Faisalabad is a large industrial city with little public data.", ["epic_pu"], ["epic_punjab-univ"], functions="monitoring; research", profit="public",
   hq="pakistan", countries="pakistan", places="Faisalabad", domains="ambient monitoring; industrial emissions", roles="evidence", sclass="funder-reported", period="2025-"),
 O("habib-university", "Habib University", "research", "Academic institution", "Leading 'SindhAir', Karachi's first open continuous air monitoring network, with the Sindh Environmental Protection Agency (EPIC 2026 award).",
   "Karachi has more than 20 million people and little public real-time data.", ["epic_habib"], ["epic_habib"], functions="monitoring; research",
   hq="pakistan", countries="pakistan", places="Karachi (industrial zones, port, schools)", domains="ambient monitoring; schools and childcare", roles="evidence",
   sclass="funder-reported", period="2026-"),
 O("sindh-epa", "Sindh Environmental Protection Agency", "public", "Provincial environmental regulator", "Partner for reference-grade monitoring in Karachi's SindhAir network.",
   "The regulator is the body that can enforce Sindh's air standards.", ["epic_habib"], ["epic_habib"], functions="enforcement; monitoring", profit="public",
   hq="pakistan", countries="pakistan", places="Karachi", domains="ambient monitoring", roles="accountability", sclass="partner-reported", period="2026-"),
 O("ndma-neoc", "National Emergencies Operation Center (NDMA, Pakistan)", "public", "National disaster agency cell", "Partner for 70 PAQI-installed PM2.5 monitors used for real-time risk monitoring.",
   "Treating smog as a disaster risk brings in emergency systems.", ["epic_paqi"], ["epic_paqi"], functions="monitoring", profit="public",
   hq="pakistan", countries="pakistan", domains="ambient monitoring", roles="protect-health", sclass="partner-reported", period="2025-"),
 # ---- Bangladesh
 O("bela", "Bangladesh Environmental Lawyers Association (BELA)", "ngo", "Environmental legal NGO", "Uses the courts on pollution: won a 2020 order closing an illegal Jashore brick kiln, and partners on Dhaka landfill-burning monitoring.",
   "Litigation can force regulators to act where enforcement is weak.", ["bela_kiln", "epic_sab"], ["tbs_bela", "epic_smart-air-bangladesh"],
   functions="advocacy and litigation", hq="bangladesh", countries="bangladesh", places="Jashore; Dhaka", domains="brick kilns; waste/open burning; rights and legal enforcement",
   roles="accountability", period="2018-", sclass="journalism and partner account", outcomes="One kiln closure ordered (2020); compliance not checked"),
 O("hrpb", "Human Rights and Peace for Bangladesh (HRPB)", "ngo", "Public-interest litigation NGO", "Filed the 2019 writ that led the High Court to order twice-weekly mobile courts against Dhaka's air polluters.",
   "Court orders put deadlines on the Department of Environment.", ["hrpb"], ["tbs_hrpb"], functions="advocacy and litigation", hq="bangladesh", countries="bangladesh",
   places="Dhaka", domains="rights and legal enforcement; brick kilns", roles="accountability", period="2019-", sclass="journalism",
   outcomes="Court orders issued; enforcement results not established"),
 O("smart-air-bangladesh", "Smart Air Bangladesh", "private", "Social enterprise (air quality)", "Installing monitors around Dhaka's two biggest landfills to show how much waste burning adds to the city's air pollution (EPIC 2026 award).",
   "Evidence to enforce existing bans on open burning.", ["epic_sab"], ["epic_smart-air-bangladesh"], functions="monitoring; advocacy", profit="unclear",
   hq="bangladesh", countries="bangladesh", places="Matuail and Aminbazar landfills, Dhaka", domains="waste/open burning; ambient monitoring",
   communities="Residents near landfills", roles="evidence; accountability", sclass="funder-reported", period="2026-", partners="BIGD; BELA"),
 O("obhizatrik", "OBHIZATRIK Foundation", "ngo", "Youth-led foundation", "Placing air sensors in Dhaka's informal settlements and industrial areas and publishing every reading live ('Breathing Dhaka', EPIC 2026 award).",
   "Measures air where the poorest residents live, which official stations miss.", ["epic_obh"], ["epic_obhizatrik"], functions="monitoring; advocacy",
   hq="bangladesh", countries="bangladesh", places="Dhaka informal settlements and industrial zones", domains="ambient monitoring; community-led monitoring",
   communities="Residents of informal settlements", roles="evidence; accountability", sclass="funder-reported", period="2026-"),
 O("bigd", "BRAC Institute of Governance and Development (BIGD)", "research", "University research institute", "Research partner in Smart Air Bangladesh's landfill-burning monitoring project.",
   "Links measurement to governance research.", ["epic_sab"], ["epic_smart-air-bangladesh"], functions="research", hq="bangladesh", countries="bangladesh",
   places="Dhaka", domains="waste/open burning", roles="evidence", sclass="partner-reported", period="2026-"),
 O("caps-stamford", "Center for Atmospheric Pollution Studies (CAPS), Stamford University Bangladesh", "research", "University research centre",
   "Tracks Dhaka's air quality over time; reported only 38 days of acceptable air in 2016-2021.", "Long records show how persistent the problem is.",
   ["caps"], ["tbs_caps"], functions="research; monitoring", hq="bangladesh", countries="bangladesh", places="Dhaka; 64 districts",
   domains="ambient monitoring", roles="evidence", sclass="journalism", period="2016-", aliases="CAPS"),
 O("university-of-dhaka", "University of Dhaka", "research", "Academic institution", "Partner in a black-carbon science grant led by Stockholm University (2024-2027).",
   "Brings Bangladeshi scientists into regional black-carbon research.", ["caf_bc"], ["caf1"], functions="research", profit="public",
   hq="bangladesh", countries="bangladesh", domains="source apportionment", roles="evidence", sclass="funder-reported", period="2024-2027"),
 # ---- Indonesia
]
NEW += [
 O("bicara-udara", "Bicara Udara (Yayasan Udara Anak Bangsa)", "ngo", "National NGO (foundation)", "A non-profit that campaigns for cleaner-air policy through ambassadors, public talks and a schools alliance.",
   "Builds public pressure for Jakarta's and Indonesia's clean-air rules.", ["bicara"], ["bicara"], functions="advocacy; public communication",
   hq="indonesia", countries="indonesia", places="Jakarta", domains="schools and childcare; community mobilisation", communities="Students; young people",
   roles="accountability", website="https://bicaraudara.id/", legal="Foundation (yayasan)", period="2026", outputs="Reach figures published by the organisation (not verified)"),
 O("nafas-indonesia", "Nafas Indonesia (company)", "private", "Company: air quality data and app", "A company that runs a large network of outdoor air sensors in Greater Jakarta and other cities and shares readings through an app.",
   "Gives residents street-level readings; the company also sells data services and sponsorship.", ["nafas_co", "nafas_dbs", "dbs_grant"],
   ["nafas_about", "airly_nafas", "nafas_dbs", "dbs50"], functions="monitoring; technology supply; public communication", profit="for-profit",
   legal="Private company (described as a startup by DBS)", hq="indonesia", countries="indonesia", places="Greater Jakarta and 20+ cities",
   domains="ambient monitoring; data systems", roles="evidence", website="https://nafas.co.id/", sclass="company-reported", brole="A: solution provider (data)",
   itest="Calibration against reference stations is company-reported; no independent evaluation found", conflict="Sensor data are sponsored; keep separate from Nafas Foundation",
   aliases="NAFAS", outcomes="Activity documented; outcome not independently evaluated"),
 O("nafas-foundation", "Nafas Foundation", "ngo", "Non-profit initiative of a company", "A non-profit set up by Nafas Indonesia that now runs the sensor network's public data, research and education work.",
   "Separating the non-profit from the company matters for who is accountable for the data.", ["nafas_fd", "nafas_pneu"], ["nafas_found", "dbs_pneu"],
   functions="monitoring; research; public communication", hq="indonesia", countries="indonesia", places="23 cities (as stated)", domains="ambient monitoring",
   roles="evidence", website="https://nafas.foundation/", sclass="organisation-reported", legal="Non-profit initiative (legal form not stated)",
   conflict="Founded by, and closely linked to, Nafas Indonesia (company)"),
 O("airly", "Airly", "private", "Company: sensor manufacturer (Europe)", "Supplies the outdoor sensors used in Nafas's Jakarta network.",
   "A supplier, not an operator: who maintains and calibrates matters.", ["nafas_co"], ["nafas_about", "airly_nafas"], functions="technology supply",
   profit="for-profit", legal="Private company", hq="global", countries="indonesia", domains="ambient monitoring", roles="evidence", sclass="company-reported",
   brole="A: technology supplier", itest="No independent test of the Jakarta deployment found"),
 O("fkm-ui", "Faculty of Public Health, Universitas Indonesia", "research", "Academic institution", "Co-authored a 2025 white paper with Nafas and DBS Foundation linking PM2.5 to pneumonia among Jakarta's under-fives.",
   "Brings health data into Jakarta's air debate; the study shows association, not cause.", ["nafas_pneu"], ["dbs_pneu"], functions="research",
   profit="public", hq="indonesia", countries="indonesia", places="Jakarta", domains="health facilities; respiratory care", communities="Children under five",
   roles="evidence; protect-health", sclass="partner-reported", aliases="FKM UI", period="2025"),
 O("koalisi-ibukota", "Koalisi Ibukota (Capital City Coalition)", "community", "Citizens' coalition", "The citizens' coalition that won the Jakarta air pollution lawsuit; courts found seven officials negligent and the Supreme Court upheld it in 2023.",
   "Shows that residents can hold the national government legally responsible for air quality.", ["jkt_suit", "jkt_kasasi"], ["gp_sea", "gp_kasasi"],
   functions="advocacy and litigation", hq="indonesia", countries="indonesia", places="Jakarta", domains="rights and legal enforcement",
   communities="Jakarta residents", roles="accountability", period="2019-2023", sclass="organisation-reported",
   outcomes="Court ruling won (2021, upheld 2023); implementation not established"),
 O("greenpeace-indonesia", "Greenpeace Indonesia", "ngo", "International NGO (national office)", "Publicised and supported the Jakarta citizens' lawsuit and campaigns for the court ruling to be implemented.",
   "Keeps the court ruling in public view.", ["jkt_suit", "jkt_kasasi"], ["gp_sea", "gp_kasasi"], functions="advocacy", hq="indonesia",
   countries="indonesia", places="Jakarta", domains="rights and legal enforcement", roles="accountability", period="2019-", sclass="organisation-reported"),
 # ---- Thailand
 O("thailand-can", "Thailand Clean Air Network (Thailand CAN)", "community", "Citizen network (registered association)", "Citizens and academics who drafted one of the clean-air laws Thailand's cabinet approved for parliament in 2023.",
   "Its draft helped put a national clean-air law on the agenda; the law was still not enacted at the cutoff.", ["tcan", "tcan_bill", "th_bill"],
   ["tcan", "wiki_tcab", "nation_house", "nation_joint"], functions="advocacy; research; policy drafting", hq="thailand", countries="thailand",
   places="Bangkok; national", domains="rights and legal enforcement", roles="accountability", website="https://thailandcan.net/",
   legal="Association (Thai name: สมาคมเครือข่ายอากาศสะอาดเพื่อสุขภาพ)", period="2019-", sclass="organisation-reported and journalism",
   outcomes="Bill passed the House (2025); not enacted at cutoff"),
 O("chiang-mai-breath-council", "Chiang Mai Breath Council", "network", "Multi-sector civic council", "A council set up in 2019 by health, business and civil-society groups to tackle Chiang Mai's seasonal smoke haze.",
   "Northern Thailand's haze comes from fires that local communities and officials both manage.", ["cmbc"], ["prachatai_cm"],
   functions="advocacy; community mobilisation", hq="thailand", countries="thailand", places="Chiang Mai", domains="forest/peat haze; crop residue and agriculture",
   communities="Residents of northern Thailand", roles="reduce-emissions; accountability", period="2019-", sclass="journalism"),
 # ---- Viet Nam
 O("live-and-learn-vietnam", "Live & Learn Vietnam (Center for Living and Learning for Environment and Community)", "ngo", "National NGO", "Runs a green schools programme in Hanoi on air pollution and waste, reported in 93 schools of Dong Anh district.",
   "Schools reach children and families; air-quality change has not been measured.", ["ll_green"], ["livelearn"], functions="public communication; service delivery",
   hq="vietnam", countries="vietnam", places="Hanoi (Dong Anh and three other districts)", domains="schools and childcare; waste/open burning",
   communities="Schoolchildren", roles="reduce-exposure", period="2021-2023", sclass="organisation-reported", status="historical (funding after 2025 not established)"),
 O("winrock", "Winrock International", "ngo", "International NGO (implementer)", "Led USAID's Reducing Pollution project in Viet Nam on open burning, craft-village furnaces and vehicle emission rules.",
   "Targets sources that city monitoring often misses, such as craft villages.", ["winrock"], ["winrock"], functions="technical assistance",
   hq="global", countries="vietnam", places="Northern Viet Nam (incl. Binh Yen craft village)", domains="industrial emissions; waste/open burning; transport/freight/e-mobility",
   roles="reduce-emissions", period="2021-2023", sclass="organisation-reported", status="historical (USAID funding after 2025 not established)"),
 O("vesdi", "VESDI (Viet Nam Environment and Sustainable Development Institute)", "research", "National research institute", "Partner on cleaner aluminium-recycling furnaces at Binh Yen craft village under USAID's Reducing Pollution project.",
   "Craft villages expose whole communities to furnace smoke.", ["winrock"], ["winrock"], functions="technical assistance; research", hq="vietnam",
   countries="vietnam", places="Binh Yen", domains="industrial emissions", communities="Craft-village households", roles="reduce-emissions",
   period="2023", sclass="partner-reported", status="historical"),
 O("usaid", "USAID", "funder", "Bilateral donor (United States)", "Funded clean-air projects in Viet Nam, including CAfCA (Hanoi green schools) and Reducing Pollution.",
   "A major past funder whose continued support after 2025 is not established in sources read.", ["ll_green", "winrock"], ["livelearn", "winrock"],
   functions="financing", profit="public", hq="global", countries="vietnam", domains="schools and childcare; industrial emissions", roles="reduce-emissions",
   status="historical", period="2017-2023", sclass="partner-reported"),
 # ---- Philippines
 O("clean-air-asia", "Clean Air Asia", "ngo", "Regional NGO", "Leads the consortium carrying out the Philippines' GEF-funded E-Mobility ASAP project and earlier produced guidance for small industries in Delhi.",
   "A regional technical NGO active in many countries.", ["emob_cons", "caf_2021"], ["sunstar", "caf19"], functions="technical assistance; research",
   hq="regional", countries="philippines;india", domains="transport/freight/e-mobility; industrial emissions", roles="reduce-emissions",
   website="https://cleanairasia.org/", sclass="journalism and funder account", period="2021-",
   conflict="Own website blocked automated access; roles taken from funder and press records"),
 O("unido", "UNIDO", "multilateral", "UN agency", "GEF implementing agency for the Philippines e-mobility project (approved for implementation July 2022).",
   "Manages GEF money and the consortium.", ["gef_emob", "emob_cons"], ["gef10609", "sunstar"], functions="technical assistance; financing", profit="intergovernmental",
   hq="global", countries="philippines", domains="transport/freight/e-mobility", roles="reduce-emissions", sclass="official", period="2022-"),
 O("dti-philippines", "Department of Trade and Industry (Philippines)", "public", "National ministry", "Government executing agency for the e-mobility project, with the Board of Investments.",
   "Industrial policy for electric vehicles sits with this ministry.", ["gef_emob", "emob_cons"], ["gef10609", "sunstar"], functions="policy-making",
   profit="public", hq="philippines", countries="philippines", domains="transport/freight/e-mobility", roles="reduce-emissions", sclass="official", period="2022-"),
 O("dlsu", "De La Salle University", "research", "Academic institution", "Consortium member of the Philippines e-mobility project.",
   "Research and testing capacity for electric vehicles.", ["emob_cons"], ["sunstar"], functions="research", hq="philippines", countries="philippines",
   domains="transport/freight/e-mobility", roles="reduce-emissions", sclass="journalism", period="2024-"),
 O("evap", "Electric Vehicle Association of the Philippines", "private", "Industry association", "Consortium member of the Philippines e-mobility project.",
   "Represents the businesses that would make and sell electric vehicles.", ["emob_cons"], ["sunstar"], functions="advocacy", profit="business association",
   hq="philippines", countries="philippines", domains="transport/freight/e-mobility", roles="reduce-emissions", sclass="journalism", period="2024-",
   brole="A: association of solution providers", conflict="Members benefit commercially from EV incentives"),
 O("uemi", "Urban Electric Mobility Initiative (UEMI)", "ngo", "International non-profit", "Consortium member of the Philippines e-mobility project.",
   "Brings urban electric mobility expertise.", ["emob_cons"], ["sunstar"], functions="technical assistance", hq="global", countries="philippines",
   domains="transport/freight/e-mobility", roles="reduce-emissions", sclass="journalism", period="2024-"),
 O("hcwh-sea", "Health Care Without Harm Southeast Asia", "ngo", "Regional health NGO", "Organised the 2025 Walk for Clean Air in Quezon City with 350 Pilipinas to demand updated air quality standards.",
   "Health workers press for standards that have not been updated in years.", ["walk"], ["walk350"], functions="advocacy", hq="philippines",
   countries="philippines", places="Quezon City", domains="health facilities", roles="protect-health; accountability", sclass="organisation-reported", period="2025"),
 O("350-pilipinas", "350 Pilipinas", "ngo", "Climate campaign group", "Co-organised the 2025 Walk for Clean Air in Quezon City.",
   "Links climate campaigning to local air quality.", ["walk"], ["walk350"], functions="advocacy; community mobilisation", hq="philippines",
   countries="philippines", places="Quezon City", domains="community mobilisation", roles="accountability", sclass="organisation-reported", period="2025"),
 O("ateneo-asmph", "Ateneo School of Medicine and Public Health", "research", "Academic institution", "Setting up Cebu City's first dense low-cost sensor network with the city government, to drive public health warnings and a local ordinance (EPIC 2026).",
   "Connects measurement to a named local decision.", ["epic_ateneo"], ["epic_ateneo"], functions="monitoring; research; health protection", hq="philippines",
   countries="philippines", places="Cebu City", domains="ambient monitoring", roles="evidence; protect-health", sclass="funder-reported", period="2026-"),
 # ---- Tier 2 and regional
 O("thingsnode", "ThingsNode", "private", "Company: environmental data", "Installing PM2.5 sensors along Sri Lanka's busiest transport corridors and publishing the data (EPIC 2026 award).",
   "Sri Lanka has little continuous roadside data.", ["epic_tn"], ["epic_thingsnode"], functions="monitoring; technology supply", profit="unclear",
   hq="sri-lanka", countries="sri-lanka", domains="transport/freight/e-mobility; ambient monitoring", roles="evidence", sclass="funder-reported", period="2026-",
   brole="A: data services"),
 O("sherubtse-college", "Sherubtse College (Royal University of Bhutan)", "research", "Academic institution", "Deploying low-cost PM2.5 monitors at 15 locations across Bhutan with ministry partners (EPIC 2025 award).",
   "Bhutan's first wide public PM2.5 coverage outside a few stations.", ["epic_sher"], ["epic_sherubtse"], functions="monitoring", profit="public",
   hq="bhutan", countries="bhutan", domains="ambient monitoring", roles="evidence", sclass="funder-reported", period="2025-"),
 O("upm-goaqs", "Universiti Putra Malaysia and GO AQS", "research", "University-led partnership", "Generating evidence on at-risk communities to strengthen Malaysia's Clean Air Action Plan ('AIRCHAMP', EPIC 2026).",
   "Moves from monitoring to prevention in national policy.", ["epic_upm"], ["epic_upm"], functions="research; monitoring", hq="malaysia",
   countries="malaysia", domains="ambient monitoring; health facilities", roles="evidence", sclass="funder-reported", period="2026-"),
 O("maldives-climate-observatory", "Maldives Climate Observatory", "research", "Atmospheric observatory", "Partner in a Stockholm University-led black-carbon science grant (2024-2027).",
   "Measures pollution carried over the Indian Ocean from South Asia.", ["caf_bc"], ["caf1"], functions="research; monitoring", hq="maldives",
   countries="maldives", domains="source apportionment", roles="evidence", sclass="funder-reported", period="2024-2027"),
 O("acc-thpc", "ASEAN Coordinating Centre for Transboundary Haze Pollution Control", "multilateral", "Regional intergovernmental centre", "ASEAN's centre for coordinating action on smoke haze from land and forest fires, soft-launched in 2023.",
   "Haze crosses borders, so no single country can solve it alone.", ["acc"], ["asean_acc"], functions="policy-making; coordination", profit="intergovernmental",
   hq="indonesia", countries="indonesia;malaysia;singapore;thailand", domains="forest/peat haze", roles="reduce-emissions; accountability", sclass="official",
   period="2023-", status="announced (soft launch 2023; full operation not confirmed)", aliases="ACC THPC"),
 O("crea", "Centre for Research on Energy and Clean Air (CREA)", "research", "Independent research organisation", "Analyses air pollution trends, causes and health effects for governments, companies and campaigners across Asia and Europe.",
   "Frequently cited analysis of pollution sources.", ["crea"], ["crea"], functions="research", hq="regional", countries="india;indonesia;thailand;vietnam;philippines",
   domains="source apportionment", roles="evidence", website="https://energyandcleanair.org/", sclass="organisation-reported", period="2026",
   conflict="Funded partly by commissioned research"),
 O("openaq", "OpenAQ", "ngo", "Open-data non-profit", "Runs the open platform where several Asian monitoring projects publish their readings.",
   "Open data lets anyone check official figures.", ["openaq", "cun_proj", "epic_habib"], ["openaq", "cun", "epic_habib"], functions="data systems",
   hq="global", countries="nepal;pakistan", domains="data systems", roles="evidence", website="https://openaq.org/", sclass="organisation-reported"),
]

NEW += [O("gef", "Global Environment Facility (GEF)", "multilateral", "Multilateral environment fund",
   "Approved a US$3.79 million grant in 2022 for the Philippines e-mobility project, implemented by UNIDO.",
   "Climate funds pay for transport projects whose air-quality benefits are usually not measured.", ["gef_emob"], ["gef10609"],
   functions="financing", profit="intergovernmental", hq="global", countries="philippines", domains="transport/freight/e-mobility",
   roles="reduce-emissions", sclass="official", funder_id="gef", period="2022-")]
# ---------- projects (J) ----------
def J(pid, title, desc, country, location, domain, ints, start, end, status, groups, intended, activities, outputs, outcomes, evaluation,
      aq, funding, limits, claims, airshed="", cost="", cur="", ctype="", owner=""):
    return dict(project_id=pid, title=title, short_plain_language_description=desc, intervention_ids=ints, domain=domain,
                country=country, specific_location=location, airshed=airshed, start_date=start, end_date=end, status=status,
                target_groups=groups, intended_change=intended, activities=activities, outputs_reported=outputs,
                outcomes_measured=outcomes, evaluation_type=evaluation, air_quality_objective=aq, cost_amount=cost,
                cost_currency=cur, cost_type=ctype, continuing_cost_owner=owner or "Not established", funding_visibility=funding,
                limitations=limits, claim_ids=";".join(cl[k] for k in claims),
                source_ids=";".join(sorted({sid for k in claims for sid in next(r for r in claim_rows() if r['claim_id']==cl[k])['source_ids'].split(';')})))
_rows = None
def claim_rows():
    global _rows
    if _rows is None: _rows = list(csv.DictReader(open(reg.CLM)))
    return _rows
NOT = "No adequate evidence found"
MEAS = "Measurement only: no exposure, health or policy outcome reported"
PROJ = [
 J("J001", "Breathing Easier: PM2.5 in Kathmandu schools", "Sensors in 40 Kathmandu schools, open data and awareness sessions for students and teachers.", "nepal", "Kathmandu", "schools and childcare",
   "low-cost-sensors-action;school-education", "2025-02-01", "", "completed (as listed)", "Schoolchildren; teachers", "Policy attention to children's exposure",
   "Sensor installation; dashboard; awareness sessions; health camps; policy brief", "40 sensors; 1,500 students and 80 teachers reached (organisation-reported)", MEAS, "None", "primary",
   "Grant amount not public", "Outputs are self-reported; measurement in schools is not a reduction in children's exposure or illness.", ["cun_proj", "epic_gdl"]),
 J("J002", "Clean Energy Nepal low-cost monitoring network", "Low-cost PM2.5 monitors with municipalities in cities across Nepal, with open data and youth outreach.", "nepal", "10+ cities incl. provincial capitals", "ambient monitoring",
   "low-cost-sensors-action;community-led-monitoring", "2025", "", "operating (as described)", "Urban residents; municipalities", "Data for national and local air quality plans",
   "Install 21 monitors (EPIC); dashboard in Nepali; train youth", "Planned: 21 monitors (EPIC award)", MEAS, "None", "primary", "Grant amount not public",
   "Programme page is undated; funder of the earlier 10-city plan not stated.", ["epic_cen", "cen_shp"]),
 J("J003", "PAQI national monitor expansion with NDMA", "Seventy affordable PM2.5 monitors installed with Pakistan's national emergencies centre.", "pakistan", "National", "ambient monitoring",
   "low-cost-sensors-action", "2025", "", "operating (as described)", "General public; disaster managers", "Better data for the National Clean Air Policy",
   "Install monitors; publish open data", "Planned: 70 monitors", MEAS, "None", "primary", "Grant amount not public", "Funder page describes plans, not results.", ["epic_paqi"]),
 J("J004", "Urban Unit 10-city sensor network", "160 low-cost monitors across 10 Pakistani cities with an open portal and health advisories.", "pakistan", "10 cities", "ambient monitoring",
   "low-cost-sensors-action", "2025", "", "operating (as described)", "City residents; local governments", "City-level action plans", "Install monitors; open portal; advisories",
   "Planned: 160 monitors", MEAS, "None", "primary", "Grant amount not public", "Plans only in source read.", ["epic_uu"]),
 J("J005", "Faisalabad's first air monitoring network", "Ten low-cost monitors in Faisalabad's industrial, commercial and residential areas.", "pakistan", "Faisalabad", "ambient monitoring",
   "low-cost-sensors-action", "2025", "", "operating (as described)", "Residents of an industrial city", "Identify hotspots; advocate stricter standards", "Install monitors",
   "Planned: 10 monitors", MEAS, "None", "primary", "Grant amount not public", "Plans only in source read.", ["epic_pu"]),
 J("J006", "SindhAir: Karachi open monitoring", "Open continuous PM2.5 monitoring across Karachi's industry, port, traffic corridors and schools.", "pakistan", "Karachi", "ambient monitoring",
   "low-cost-sensors-action", "2026", "", "starting (awarded Oct 2026)", "Karachi residents; schoolchildren", "Enforcement of Sindh air standards", "Sensors; reference monitoring with Sindh EPA; OpenAQ",
   "None yet", MEAS, "None", "primary", "Grant amount not public", "Newly awarded; no outputs yet.", ["epic_habib"]),
 J("J007", "Landfill-burning monitoring in Dhaka", "Monitors around Matuail and Aminbazar landfills to measure the contribution of waste burning.", "bangladesh", "Dhaka", "waste/open burning",
   "low-cost-sensors-action", "2026", "", "starting (awarded Oct 2026)", "Residents near landfills", "Enforcement of laws against open burning", "Sensors plus wind and satellite data; legal use with BELA",
   "None yet", MEAS, "None", "primary", "Grant amount not public", "Newly awarded.", ["epic_sab"]),
 J("J008", "Breathing Dhaka: sensors in informal settlements", "Live, open air readings from Dhaka's informal settlements and industrial areas.", "bangladesh", "Dhaka", "ambient monitoring",
   "community-led-monitoring", "2026", "", "starting (awarded Oct 2026)", "Residents of informal settlements", "Put evidence before policymakers", "Sensors; open data",
   "None yet", MEAS, "None", "primary", "Grant amount not public", "Newly awarded.", ["epic_obh"]),
 J("J009", "Bhutan national PM2.5 sensor network", "Low-cost monitors at 15 locations across Bhutan.", "bhutan", "15 locations", "ambient monitoring", "low-cost-sensors-action", "2025", "",
   "operating (as described)", "Residents", "Data for policy", "Install monitors; open data", "Planned: 15 locations", MEAS, "None", "primary", "Grant amount not public", "Plans only.", ["epic_sher"]),
 J("J010", "Sri Lanka transport-corridor PM2.5 monitoring", "Sensors along busy Sri Lankan roads, data shared freely.", "sri-lanka", "Transport corridors", "transport/freight/e-mobility",
   "low-cost-sensors-action", "2026", "", "starting (awarded Oct 2026)", "Road users; roadside residents", "Update outdated air rules", "Sensors; open data", "None yet", MEAS, "None", "primary",
   "Grant amount not public", "Newly awarded.", ["epic_tn"]),
 J("J011", "AIRCHAMP (Malaysia)", "Evidence on air pollution and at-risk communities to strengthen Malaysia's Clean Air Action Plan.", "malaysia", "National", "ambient monitoring",
   "low-cost-sensors-action", "2026", "", "starting (awarded Oct 2026)", "At-risk communities", "Stronger national air governance", "Monitoring; research; policy engagement", "None yet", MEAS, "None", "primary",
   "Grant amount not public", "Newly awarded.", ["epic_upm"]),
 J("J012", "Cebu City sensor network and ordinance", "Dense low-cost network, public health warnings and a first local air quality ordinance.", "philippines", "Cebu City", "ambient monitoring",
   "low-cost-sensors-action", "2026", "", "starting (awarded Oct 2026)", "Cebu City residents", "Warnings and a local ordinance", "Sensors; warnings; ordinance support", "None yet", MEAS, "None", "primary",
   "Grant amount not public", "Newly awarded.", ["epic_ateneo"]),
 J("J013", "Women AQI ambassadors in Delhi's settlements", "Women from unrecognised settlements trained to measure air with portable monitors and inform neighbours.", "india", "Delhi resettlement and unrecognised settlements", "outdoor workers",
   "worker-community-voice;community-led-monitoring", "2021", "", "operating (2024 report)", "Women residents and workers", "Awareness and access to protection", "Training; portable monitoring; door-to-door drives; meetings",
   "8-9 active ambassadors reported (2024)", NOT, "None", "primary", "Funded through Clean Air Fund grants (amounts not public)", "Exposure, health and income effects were not measured.", ["hdb_aqi", "caf_mht23"]),
 J("J014", "Indi-SET independent sensor evaluation", "Independent co-location testing of low-cost sensors against a reference monitor in Bengaluru.", "india", "Bengaluru", "ambient monitoring",
   "independent-evaluation;low-cost-sensors-action", "2023-12", "", "operating", "Cities, regulators and funders buying sensors", "Reliable sensor data before deployment",
   "Co-location testing; calibration; training", "48 devices from six manufacturers tested (2026 report)", "Independent test: no manufacturer met NO2 and O3 precision targets", "Independent performance evaluation", "primary",
   "Funding of the facility not established in sources read", "Tests measurement accuracy only; says nothing about emission or exposure reduction.", ["indiset", "indiset_eval"]),
 J("J015", "10-city Atmos sensor network (India)", "Sensor-based PM2.5 and PM10 network across 10 Indian cities.", "india", "10 cities", "ambient monitoring", "low-cost-sensors-action", "2017-12", "2021", "completed",
   "City residents; researchers", "Adoption of affordable monitoring", "Deploy and validate sensors", "10-city network (company/funder report)", MEAS, "None found", "primary", "Shakti Foundation funded (amount not public)",
   "Funder/company report; not independently evaluated.", ["respirer"]),
 J("J016", "Nafas sensor expansion with DBS Foundation", "Fifty new outdoor sensors in Indonesian cities beyond Jakarta.", "indonesia", "Medan, Pekanbaru, Palembang, Pontianak, Balikpapan, Samarinda, Makassar, Manado and others", "ambient monitoring",
   "low-cost-sensors-action", "2024-08", "", "operating (19 of 50 installed by Sept 2024)", "City residents", "Public awareness of air quality", "Install sensors; app data",
   "19 of 50 sensors installed by Sept 2024 (organisation-reported)", MEAS, "None", "primary", "DBS Foundation grant (amount not public in sources read; grant cap SGD 250,000 stated for a later round)",
   "Company-run network; sponsor-hosted sites; no independent data-quality audit found.", ["dbs_grant", "nafas_dbs"]),
 J("J017", "Jakarta PM2.5 and child pneumonia white paper", "Analysis linking PM2.5 to pneumonia prevalence in Jakarta's under-fives.", "indonesia", "Jakarta", "respiratory care", "health-readiness", "2025", "2025-07", "completed",
   "Children under five", "Evidence for health-sector action", "Data analysis; white paper", "White paper published (July 2025)", "Association reported (not causal)", "Not peer reviewed", "primary",
   "DBS Foundation support (amount not public)", "Association in sub-district data; not a causal estimate.", ["nafas_pneu"]),
 J("J018", "Citizens' Lawsuit on Jakarta Air Pollution", "Residents sued national and provincial officials for failing to control Jakarta's air pollution.", "indonesia", "Jakarta", "rights and legal enforcement",
   "", "2019-07", "2023-11", "ruling won; implementation not established", "Jakarta residents", "Court-ordered government action", "Litigation", "District court ruling (2021); appeals rejected (2023)",
   "Legal outcome only; air-quality effect not measured", "None", "primary", "Not applicable", "Winning a ruling is not the same as compliance.", ["jkt_suit", "jkt_kasasi"]),
 J("J019", "Thailand Clean Air Bill (citizen draft)", "A citizen network's draft clean-air law, one of seven taken to parliament.", "thailand", "National", "rights and legal enforcement", "airshed-management-plans",
   "2023", "", "pending (joint committee, Sept 2026)", "Everyone in Thailand", "A national clean-air law", "Drafting; advocacy", "Draft approved by cabinet for parliament (2023); House passed bill (2025)",
   "Law not enacted at cutoff", "None", "primary", "Not applicable", "A bill passed by one chamber is not an enacted or enforced law.", ["tcan_bill", "th_bill"]),
 J("J020", "Zigzag kiln rebuilding in Nepal", "Design manual and support for rebuilding earthquake-damaged brick kilns as cleaner zigzag kilns.", "nepal", "Kathmandu Valley and beyond", "brick kilns", "kiln-transition",
   "2015", "", "historical", "Kiln owners; workers; nearby residents", "Lower coal use and emissions", "Design manual; training; regional exchange", "Manual published (2015); regional exchange (2018)",
   "Stated potential coal saving up to 30% (not a measured result in sources read)", "None found", "primary", "Not public", "No evaluation of emissions across rebuilt kilns, or of workers' conditions, in sources read.",
   ["kiln_np", "kiln_reg"], airshed="Indo-Gangetic Plain and Himalayan Foothills"),
 J("J021", "Building Green Schools for a Green Hanoi", "School programme on air pollution, waste and green spaces in Hanoi.", "vietnam", "Hanoi (Dong Anh and three districts)", "schools and childcare", "school-education",
   "2021", "", "historical (support after 2025 not established)", "Schoolchildren", "Awareness and school practices", "Clean Air Week; Green Ambassador competition; school measures",
   "69+ schools, then all 93 in Dong Anh (organisation-reported)", NOT, "None", "co-benefit", "USAID-funded CAfCA (amount not public in source read)", "No air-quality or exposure measurement reported.", ["ll_green"]),
 J("J022", "USAID Reducing Pollution (Viet Nam)", "Work on open burning, craft-village furnaces and vehicle emission regulation.", "vietnam", "Northern Viet Nam", "industrial emissions",
   "industrial-boiler-transition;vehicle-inspection-maintenance", "2021", "", "historical (status after 2025 not established)", "Craft-village households; residents", "Lower emissions from local sources",
   "Pilots in craft villages; open-burning work; vehicle emission roadmap", "Pilot activities described (2023)", NOT, "None", "primary", "USAID (amount not in source read)",
   "Implementer's own account; no measured results.", ["winrock"]),
 J("J023", "E-Mobility ASAP (Philippines)", "GEF-funded project to grow electric public transport, two-wheelers and battery industries.", "philippines", "National", "transport/freight/e-mobility",
   "e-bus-fleet-renewal", "2022-07-01", "2027-06", "operating", "Transport operators; drivers; industry", "Lower transport emissions (climate objective)", "Policy support; business models; charging demonstrations",
   "Not reported in sources read", NOT, "None", "co-benefit", "GEF grant US$3.79m approved; co-financing US$77.5m",
   "GEF focal area is climate change; air-quality benefit is an unmeasured co-benefit.", ["gef_emob", "emob_cons"], cost="3788990", cur="USD", ctype="GEF grant (approved)"),
 J("J024", "Walk for Clean Air (Quezon City)", "Public walk calling for updated national air quality standards.", "philippines", "Quezon City", "rights and legal enforcement", "", "2025-12-07", "2025-12-07",
   "completed", "Public; health professionals", "Updated air quality standards", "Public event with city and national agencies", "500+ participants (organisers' figure)", NOT, "None", "primary", "Not public",
   "Advocacy event; no policy change attributed.", ["walk"]),
 J("J025", "Clean Air Fund India programme grants", "Clean Air Fund grants to Indian researchers, NGOs and government support units, 2019-2023.", "india", "Delhi; Uttar Pradesh; Punjab; Rajasthan", "data systems",
   "independent-evaluation;airshed-management-plans", "2019", "2023", "historical (grant periods listed)", "Policymakers; health workers; informal-settlement residents", "Stronger clean-air action",
   "Grants for technical assistance, research, advocacy and organising", "Grant listings only", NOT, "None", "primary", "Amounts not shown in the grant database",
   "Funder's listing gives purpose, not results.", ["caf_mht23", "caf_wri", "caf_teri", "caf_epic_in", "caf_cse", "caf_cstep", "caf_iitd", "caf_icct", "caf_2021", "caf_hcwh"]),
 J("J026", "Breathe Jakarta (Breathe Cities)", "Grants to Vital Strategies and C40 to implement Breathe Cities in Jakarta, including a planned Clean Air Zone.", "indonesia", "Jakarta", "transport/freight/e-mobility",
   "airshed-management-plans", "2024", "", "operating (as described)", "Jakarta residents", "Lower transport and industrial emissions; Clean Air Zone", "Data, awareness, Clean Air Zone design",
   "Not reported", NOT, "None", "primary", "Amounts not shown", "Overlaps programme P10; funder listing only.", ["caf_jkt"]),
 J("J027", "Microsensor challenges (Thailand and India)", "Independent side-by-side evaluation of low-cost sensors.", "thailand", "Thailand; India", "ambient monitoring", "independent-evaluation", "2023", "2024", "completed (grant periods)",
   "Sensor buyers", "Informed sensor purchasing", "Co-location evaluations", "Not reported in source read", NOT, "Independent evaluation (results not read)", "primary", "Amounts not shown",
   "Results of the challenges were not read for this edition.", ["caf_airparif"]),
 J("J028", "Dhaka landfill and brick-kiln litigation", "Court cases brought by BELA and HRPB against illegal kilns and Dhaka's air pollution.", "bangladesh", "Dhaka; Jashore", "rights and legal enforcement", "", "2019", "", "ongoing (orders issued)",
   "Dhaka and Jashore residents", "Enforcement against polluters", "Writ petitions", "Court orders: mobile courts (2019); one kiln closure (2020)", "Enforcement results not established", "None", "primary", "Not applicable",
   "Orders are not proof of compliance.", ["bela_kiln", "hrpb"]),
]

# ---------- roles ----------
def R(org, pid, role, desc, keys, ver="documented"):
    return dict(organisation_id=org, project_id=pid, role=role, role_description=desc, source_ids=";".join(src[k] for k in keys), verification_status=ver)
ROLES = [
 R("clean-up-nepal", "J001", "implementer", "Project lead", ["cun"]), R("gd-labs", "J001", "technical partner", "Consortium partner; EPIC awardee for 40 school monitors", ["cun", "epic_gdlabs"]),
 R("epic-aq-fund", "J001", "grantmaker", "Funding/support organisation", ["cun", "epic_gdlabs"]), R("openaq", "J001", "technical partner", "Hosts the open data", ["cun"]),
 R("clean-energy-nepal", "J002", "implementer", "Installs monitors with government partners", ["epic_cen", "cen_shp"]), R("epic-aq-fund", "J002", "grantmaker", "2025 award", ["epic_cen"]),
 R("paqi", "J003", "implementer", "Installs and runs monitors", ["epic_paqi"]), R("ndma-neoc", "J003", "public duty holder", "Partner for real-time risk monitoring", ["epic_paqi"]),
 R("epic-aq-fund", "J003", "grantmaker", "2025 award", ["epic_paqi"]),
 R("urban-unit", "J004", "implementer", "Installs monitors; runs portal", ["epic_urban-unit"]), R("epic-aq-fund", "J004", "grantmaker", "2025 award", ["epic_urban-unit"]),
 R("university-of-the-punjab", "J005", "implementer", "Installs monitors", ["epic_punjab-univ"]), R("epic-aq-fund", "J005", "grantmaker", "2025 award", ["epic_punjab-univ"]),
 R("habib-university", "J006", "implementer", "Project lead", ["epic_habib"]), R("sindh-epa", "J006", "regulator", "Partner for reference-grade monitoring", ["epic_habib"]),
 R("openaq", "J006", "technical partner", "Data published via OpenAQ", ["epic_habib"]), R("epic-aq-fund", "J006", "grantmaker", "2026 award", ["epic_habib"]),
 R("smart-air-bangladesh", "J007", "implementer", "Project lead", ["epic_smart-air-bangladesh"]), R("bigd", "J007", "technical partner", "Research partner", ["epic_smart-air-bangladesh"]),
 R("bela", "J007", "delivery partner", "Legal use of evidence for enforcement", ["epic_smart-air-bangladesh"]), R("epic-aq-fund", "J007", "grantmaker", "2026 award", ["epic_smart-air-bangladesh"]),
 R("obhizatrik", "J008", "implementer", "Project lead", ["epic_obhizatrik"]), R("epic-aq-fund", "J008", "grantmaker", "2026 award", ["epic_obhizatrik"]),
 R("sherubtse-college", "J009", "implementer", "Project lead", ["epic_sherubtse"]), R("epic-aq-fund", "J009", "grantmaker", "2025 award", ["epic_sherubtse"]),
 R("thingsnode", "J010", "implementer", "Project lead", ["epic_thingsnode"]), R("epic-aq-fund", "J010", "grantmaker", "2026 award", ["epic_thingsnode"]),
 R("upm-goaqs", "J011", "implementer", "Project lead", ["epic_upm"]), R("epic-aq-fund", "J011", "grantmaker", "2026 award", ["epic_upm"]),
 R("ateneo-asmph", "J012", "implementer", "Project lead with Cebu City Government", ["epic_ateneo"]), R("epic-aq-fund", "J012", "grantmaker", "2026 award", ["epic_ateneo"]),
 R("mht", "J013", "implementer", "Trains and supports AQI ambassadors", ["ys_aqi"]), R("help-delhi-breathe", "J013", "implementer", "Co-runs ambassadors; door-to-door drives", ["ys_aqi"]),
 R("clean-air-fund", "J013", "grantmaker", "Grants to Mahila Housing (Sewa) Trust, 2021 and 2023", ["caf12", "caf19"]),
 R("cstep", "J014", "evaluator", "Runs the facility and evaluation", ["cstep_set", "cstep_pr"]),
 R("respirer", "J014", "supplier", "Devices tested", ["cstep_annex"]), R("airveda", "J014", "supplier", "Devices tested", ["cstep_annex"]), R("aurassure", "J014", "supplier", "Devices tested", ["cstep_annex"]),
 R("respirer", "J015", "implementer", "Built and ran the sensor network", ["shakti_resp"]), R("iit-kanpur", "J015", "technical partner", "Scientific partner", ["shakti_resp"]),
 R("shakti-foundation", "J015", "grantmaker", "Funded the project", ["shakti_resp"]),
 R("nafas-indonesia", "J016", "implementer", "Installs and runs sensors", ["dbs50", "nafas_dbs"]), R("dbs-foundation", "J016", "grantmaker", "Business for Impact Grant 2023", ["dbs50"]),
 R("airly", "J016", "supplier", "Sensor supplier to the Nafas network", ["nafas_about"]),
 R("nafas-foundation", "J017", "implementer", "Co-author (as Nafas Indonesia)", ["dbs_pneu"]), R("fkm-ui", "J017", "technical partner", "Co-author", ["dbs_pneu"]), R("dbs-foundation", "J017", "co-funder", "Collaborator and supporter", ["dbs_pneu"]),
 R("koalisi-ibukota", "J018", "implementer", "Plaintiff coalition", ["gp_kasasi"]), R("greenpeace-indonesia", "J018", "delivery partner", "Public campaigning on the case", ["gp_sea", "gp_kasasi"]),
 R("thailand-can", "J019", "implementer", "Drafted one of seven bills", ["wiki_tcab"]),
 R("icimod", "J020", "technical partner", "Co-developed design manual; convened exchange", ["icimod_2015", "icimod_2018"]), R("fnbi", "J020", "implementer", "Industry co-launcher", ["icimod_2015"]),
 R("minergy", "J020", "technical partner", "Design co-author", ["icimod_2015"]),
 R("live-and-learn-vietnam", "J021", "implementer", "Runs the programme", ["livelearn"]), R("usaid", "J021", "grantmaker", "Funded via CAfCA", ["livelearn"]),
 R("winrock", "J022", "implementer", "Project lead", ["winrock"]), R("vesdi", "J022", "technical partner", "Craft-village pilot partner", ["winrock"]), R("usaid", "J022", "grantmaker", "Donor", ["winrock"]),
 R("unido", "J023", "implementer", "GEF implementing agency", ["gef10609"]), R("dti-philippines", "J023", "public duty holder", "Government executing agency", ["gef10609", "sunstar"]),
 R("clean-air-asia", "J023", "delivery partner", "Consortium member (executing lead per press reports)", ["sunstar"], "documented (press)"),
 R("dlsu", "J023", "delivery partner", "Consortium member", ["sunstar"], "documented (press)"), R("evap", "J023", "delivery partner", "Consortium member", ["sunstar"], "documented (press)"),
 R("uemi", "J023", "delivery partner", "Consortium member", ["sunstar"], "documented (press)"),
 R("hcwh-sea", "J024", "implementer", "Co-organiser", ["walk350"]), R("350-pilipinas", "J024", "implementer", "Co-organiser", ["walk350"]),
 R("clean-air-fund", "J025", "grantmaker", "Funder", ["caf12", "caf13"]),
 R("cstep", "J025", "implementer", "Punjab strategies (2023)", ["caf12"]), R("teri", "J025", "implementer", "UP CAMP advisory unit (2023)", ["caf13"]),
 R("epic-india", "J025", "implementer", "Delhi policy and transport units (2023)", ["caf13"]), R("cse", "J025", "implementer", "NCAP good-practice compendium (2023)", ["caf13"]),
 R("wri-india", "J025", "implementer", "Agra and Gorakhpur accelerator (grant to World Resources Institute, 2023)", ["caf12"], "documented (grant to WRI; India entity not named)"),
 R("iit-delhi", "J025", "implementer", "Health and climate evidence (2023)", ["caf12"]), R("icct", "J025", "implementer", "TRUE Initiative Delhi (2022)", ["caf18"]),
 R("iclei-south-asia", "J025", "implementer", "NCR city leadership (2021)", ["caf19"]), R("pravah", "J025", "implementer", "Youth in urban slums (2021)", ["caf19"]),
 R("sesame-india", "J025", "implementer", "Children's voices (2021)", ["caf20"]), R("swaniti", "J025", "implementer", "Policy support (2021)", ["caf20"]),
 R("clean-air-asia", "J025", "implementer", "MSME learnings in Delhi (2021)", ["caf19"]), R("hcwh", "J025", "implementer", "Health sector (2019, 2023)", ["caf12", "caf24"]),
 R("dfcca", "J025", "delivery partner", "Partner programme named by funder", ["caf_hcw"]), R("cii", "J025", "implementer", "India CEO Forum for Clean Air (2019, 2023)", ["caf12", "caf23"]),
 R("iit-kanpur", "J025", "implementer", "Lucknow DSS (2021); ATMAN and core support (2023)", ["caf12", "caf15", "caf18"]),
 R("clean-air-fund", "J026", "grantmaker", "2024 grants", ["caf4"]), R("c40-org", "J026", "implementer", "Clean Air Zone support", ["caf4"]), R("vital-strategies", "J026", "implementer", "Implementing Breathe Cities", ["caf4"]),
 R("airparif", "J027", "evaluator", "Ran the challenges", ["caf7", "caf11"]), R("clean-air-fund", "J027", "grantmaker", "Funder", ["caf7", "caf11"]),
 R("bela", "J028", "implementer", "Petitioner (Jashore kiln)", ["tbs_bela"]), R("hrpb", "J028", "implementer", "Petitioner (Dhaka air pollution)", ["tbs_hrpb"]),
 R("mht", "P08", "implementer", "Named implementer", ["mht_cs"]), R("help-delhi-breathe", "P08", "implementer", "Named implementer", ["mht_cs"]),
 R("hcwh", "P09", "implementer", "Named implementer", ["caf_hcw"]), R("iit-kanpur", "P17", "implementer", "ATMAN Centre of Excellence", ["caf15"]),
 R("vital-strategies", "P11", "implementer", "With Jakarta Environment Agency", ["caf_idn"]),
 R("unido", "P16", "implementer", "GEF implementing agency", ["gef10609"]), R("clean-air-asia", "P16", "delivery partner", "Consortium member", ["sunstar"], "documented (press)"),
 R("world-bank", "P05", "lender", "IBRD financing approved Dec 2025", ["wb_rel"]), R("world-bank", "P06", "lender", "IBRD financing approved Dec 2025", ["wb_rel"]),
]
# Two named implementers in P10-P12 get records too (they are already named in the Funding Atlas)
NEW += [
 O("vital-strategies", "Vital Strategies", "ngo", "International public-health NGO", "Implements Breathe Cities in Jakarta and worked with the Jakarta Environment Agency on health and economic data for clean-air priorities.",
   "Turns health data into city decisions.", ["caf_jkt"], ["caf4", "caf_idn"], functions="technical assistance; research", hq="global", countries="indonesia",
   places="Jakarta", domains="transport/freight/e-mobility; data systems", roles="evidence; reduce-emissions", sclass="funder-reported", period="2024-"),
 O("c40-org", "C40 Cities", "network", "City network", "Received a 2024 grant to support Jakarta's planned Clean Air Zone under Breathe Cities.",
   "City-to-city network that can share designs across capitals.", ["caf_jkt"], ["caf4"], functions="technical assistance", hq="global", countries="indonesia",
   places="Jakarta", domains="transport/freight/e-mobility", roles="reduce-emissions", sclass="funder-reported", funder_id="c40", period="2024-"),
]

# ---------- funding flows ----------
def F(fid, funder, recip, pid, instr, keys, amount="", cur="", stage="", year="", conf="", conditions=""):
    return dict(flow_id=fid, funder_organisation_id=funder, recipient_organisation_id=recip, project_id=pid, funding_instrument=instr,
                amount=amount, original_currency=cur, commitment_or_disbursement=stage, approval_year=year, conditions_or_restrictions=conditions,
                public_source_ids=";".join(src[k] for k in keys), confidence_note=conf)
FLOWS = [
 F("FL001", "coefficient-giving", "epic-aq-fund", "", "grant", ["epic_news"], "1500000", "USD", "gift (launch)", "2024", "Recipient's own announcement"),
 F("FL002", "epic-aq-fund", "clean-up-nepal", "J001", "grant", ["cun"], stage="awarded", year="2025", conf="Recipient names funder"),
 F("FL003", "epic-aq-fund", "gd-labs", "J001", "grant", ["epic_gdlabs"], stage="awarded", year="2025", conf="Funder's awardee page"),
 F("FL004", "epic-aq-fund", "clean-energy-nepal", "J002", "grant", ["epic_cen"], stage="awarded", year="2025", conf="Funder's awardee page"),
 F("FL005", "epic-aq-fund", "paqi", "J003", "grant", ["epic_paqi"], stage="awarded", year="2025", conf="Funder's awardee page"),
 F("FL006", "epic-aq-fund", "urban-unit", "J004", "grant", ["epic_urban-unit"], stage="awarded", year="2025", conf="Funder's awardee page"),
 F("FL007", "epic-aq-fund", "university-of-the-punjab", "J005", "grant", ["epic_punjab-univ"], stage="awarded", year="2025", conf="Funder's awardee page"),
 F("FL008", "epic-aq-fund", "habib-university", "J006", "grant", ["epic_habib"], stage="awarded", year="2026", conf="Funder's awardee page"),
 F("FL009", "epic-aq-fund", "smart-air-bangladesh", "J007", "grant", ["epic_smart-air-bangladesh"], stage="awarded", year="2026", conf="Funder's awardee page"),
 F("FL010", "epic-aq-fund", "obhizatrik", "J008", "grant", ["epic_obhizatrik"], stage="awarded", year="2026", conf="Funder's awardee page"),
 F("FL011", "epic-aq-fund", "sherubtse-college", "J009", "grant", ["epic_sherubtse"], stage="awarded", year="2025", conf="Funder's awardee page"),
 F("FL012", "epic-aq-fund", "thingsnode", "J010", "grant", ["epic_thingsnode"], stage="awarded", year="2026", conf="Funder's awardee page"),
 F("FL013", "epic-aq-fund", "upm-goaqs", "J011", "grant", ["epic_upm"], stage="awarded", year="2026", conf="Funder's awardee page"),
 F("FL014", "epic-aq-fund", "ateneo-asmph", "J012", "grant", ["epic_ateneo"], stage="awarded", year="2026", conf="Funder's awardee page"),
 F("FL015", "clean-air-fund", "mht", "J013", "grant", ["caf12", "caf19"], stage="awarded", year="2021; 2023", conf="Funder's grant database (as Mahila Housing Sewa Trust / Gujarat Mahila Housing Sewa Trust)"),
 F("FL016", "shakti-foundation", "respirer", "J015", "grant", ["shakti_resp"], stage="funded", year="2017", conf="Joint project report"),
 F("FL017", "dbs-foundation", "nafas-indonesia", "J016", "grant", ["dbs50"], stage="awarded", year="2023", conf="Funder group's own release"),
 F("FL018", "usaid", "live-and-learn-vietnam", "J021", "grant", ["livelearn"], stage="funded (via CAfCA)", year="2021-2023", conf="Recipient's account"),
 F("FL019", "usaid", "winrock", "J022", "contract or grant (type not stated)", ["winrock"], stage="funded", year="2023", conf="Implementer's account"),
 F("FL020", "gef", "unido", "J023", "grant", ["gef10609"], "3788990", "USD", "approved", "2022", "GEF project record", "Co-financing of US$77,477,969 recorded separately"),
 F("FL021", "clean-air-fund", "cstep", "J025", "grant", ["caf12"], stage="awarded", year="2023", conf="Funder's grant database"),
 F("FL022", "clean-air-fund", "teri", "J025", "grant", ["caf13"], stage="awarded", year="2023", conf="Funder's grant database"),
 F("FL023", "clean-air-fund", "epic-india", "J025", "grant", ["caf13"], stage="awarded", year="2023", conf="Funder's grant database"),
 F("FL024", "clean-air-fund", "cse", "J025", "grant", ["caf13"], stage="awarded", year="2023", conf="Funder's grant database"),
 F("FL025", "clean-air-fund", "iit-delhi", "J025", "grant", ["caf12"], stage="awarded", year="2023", conf="Funder's grant database"),
 F("FL026", "clean-air-fund", "iit-kanpur", "J025", "grant", ["caf12", "caf15", "caf18"], stage="awarded", year="2021; 2023", conf="Funder's grant database"),
 F("FL027", "clean-air-fund", "icct", "J025", "grant", ["caf18"], stage="awarded", year="2022", conf="Funder's grant database"),
 F("FL028", "clean-air-fund", "hcwh", "J025", "grant", ["caf12", "caf24"], stage="awarded", year="2019; 2023", conf="Funder's grant database"),
 F("FL029", "clean-air-fund", "cii", "J025", "grant", ["caf12", "caf23"], stage="awarded", year="2019; 2023", conf="Funder's grant database"),
 F("FL030", "clean-air-fund", "iclei-south-asia", "J025", "grant", ["caf19"], stage="awarded", year="2021", conf="Funder's grant database (grant to ICLEI)"),
 F("FL031", "clean-air-fund", "pravah", "J025", "grant", ["caf19"], stage="awarded", year="2021", conf="Funder's grant database"),
 F("FL032", "clean-air-fund", "sesame-india", "J025", "grant", ["caf20"], stage="awarded", year="2021", conf="Funder's grant database"),
 F("FL033", "clean-air-fund", "swaniti", "J025", "grant", ["caf20"], stage="awarded", year="2021", conf="Funder's grant database"),
 F("FL034", "clean-air-fund", "clean-air-asia", "J025", "grant", ["caf19"], stage="awarded", year="2021", conf="Funder's grant database"),
 F("FL035", "clean-air-fund", "wri-india", "J025", "grant", ["caf12"], stage="awarded", year="2023", conf="Funder lists World Resources Institute; India entity not named"),
 F("FL036", "clean-air-fund", "vital-strategies", "J026", "grant", ["caf4"], stage="awarded", year="2024", conf="Funder's grant database"),
 F("FL037", "clean-air-fund", "c40-org", "J026", "grant", ["caf4"], stage="awarded", year="2024", conf="Funder's grant database"),
 F("FL038", "clean-air-fund", "airparif", "J027", "grant", ["caf7", "caf11"], stage="awarded", year="2023; 2024", conf="Funder's grant database"),
 F("FL039", "clean-air-fund", "university-of-dhaka", "", "grant (to Stockholm University; partner)", ["caf1"], stage="awarded to lead partner", year="2024", conf="Partner named in funder listing; direct receipt not established"),
 F("FL040", "clean-air-fund", "iit-bombay", "", "grant (with IGSD)", ["caf2"], stage="awarded", year="2025", conf="Funder's grant database"),
 F("FL041", "purpose", "help-delhi-breathe", "", "micro-grant", ["purpose_hdb"], stage="paid (as described)", year="2015", conf="Funder/agency's own account"),
]

# ---------- candidates (incl. exclusions) ----------
CAND = [
 ("GreenHub (Viet Nam)", "vietnam", "NGO", "not published", "Own site failed TLS; USAID fact sheet unreachable; role known only from search snippets", "https://www.greenhub.org.vn/cagc-en"),
 ("Viet Nam Green Generation Network", "vietnam", "Youth network", "not published", "Named only in a search snippet of a partner page", ""),
 ("GreenID (Viet Nam)", "vietnam", "NGO", "not published", "Current clean-air activity not verified from a primary page", ""),
 ("Clean Air Asia country networks", "regional", "Network", "not published", "Site returns HTTP 403 to automated access; not bypassed", "https://www.cleanairasia.org/who-we-are/country-networks"),
 ("Bangladesh Poribesh Andolon (BAPA)", "bangladesh", "NGO", "not published", "No primary page on a specific air programme reviewed", ""),
 ("Ecological Alert and Recovery - Thailand (EARTH)", "thailand", "NGO", "not published", "No programme-specific primary evidence reviewed", ""),
 ("Greenpeace Thailand", "thailand", "NGO", "not published", "Story page read did not establish a specific programme role", "https://www.greenpeace.org/thailand/story/19126/climate-pm25-battle-air-pollution-in-chiang-mai-from-bottom-up"),
 ("Lung Care Foundation (India)", "india", "NGO", "not published", "Co-founding role in Doctors for Clean Air seen only in search snippets", ""),
 ("Bucketlist; Centre for Social Equity and Inclusion (Delhi)", "india", "Community organisations", "mentioned, not profiled", "One news mention of door-to-door drives; too thin for a profile", "https://yourstory.com/herstory/2024/02/delhi-settlements-aqi-ambassadors-air-pollution"),
 ("A-PAG (Delhi)", "india", "Unclear", "not published", "Specific activity not verified", ""),
 ("Delhi construction worker unions (named)", "india", "Worker organisations", "kept as grouped record", "Named unions appear in court reporting only; baseline record construction-unions retained", ""),
 ("Waste-picker groups beyond Chintan", "india", "Worker organisations", "not published", "No primary source on air-specific activity found in this pass", ""),
 ("Pakistan worker or community groups outside Lahore", "pakistan", "Community", "coverage gap", "None found with documented air-pollution activity", ""),
 ("EVAP, UEMI, DLSU beyond consortium membership", "philippines", "Various", "profiled with membership only", "Only consortium membership documented", ""),
 ("HACCAP (Philippines health alliance)", "philippines", "Health alliance", "not published", "Launch page blocked automated access; seen in search snippet", "https://noharm-global.org/node/7462"),
 ("UNDP Viet Nam low-cost monitoring pilot", "vietnam", "UN agency", "not published", "Page returned 403", "https://www.undp.org/node/556806"),
 ("Indi-SET funders (Google; Open Philanthropy)", "india", "Funders", "not published as flow", "Acknowledgement seen only in a search snippet of a guidance PDF", ""),
 ("Lao PDR air-quality actors", "lao-pdr", "Any", "coverage gap", "No verified organisation-level activity found in this pass", ""),
 ("Myanmar air-quality actors", "myanmar", "Any", "coverage gap", "No verifiable public documentation reviewed", ""),
 ("Timor-Leste air-quality actors", "timor-leste", "Any", "coverage gap", "No verifiable public documentation reviewed", ""),
 ("Singapore haze actors (NEA, think tanks)", "singapore", "Public/research", "coverage gap", "Not researched in this pass", ""),
 ("Cambodia actors beyond IRRI (P13)", "cambodia", "Any", "coverage gap", "CCAC page blocked; no other primary source reviewed", ""),
 ("Mothers' groups in Indonesia (Bicara Udara framing)", "indonesia", "Community", "not claimed", "Bicara Udara's pages read do not describe it as a mothers' group", "https://bicaraudara.id/"),
]

# ---------- write ----------
def write(name, rows, fields):
    with open(os.path.join(D, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); [w.writerow(r) for r in rows]

orgs_path = os.path.join(D, "organisations.csv")
old = list(csv.DictReader(open(orgs_path, encoding="utf-8")))
base_cols = list(old[0].keys())
CAT = {"cpcb": "public", "caqm": "public", "dpcc": "public", "bspcb": "public", "delhi-bocw-board": "public", "dusib": "public", "ncdc-npcchh": "public",
       "moefcc-ncap": "public", "world-bank": "multilateral", "clean-air-fund": "funder", "mht": "community", "chintan": "ngo", "hcwh": "ngo", "cse": "research",
       "ceew": "research", "teri": "research", "iit-kanpur": "research", "igc-kv-trial": "research", "anti-slavery": "ngo", "wri-india": "research", "construction-unions": "community"}
FUNDER = {"world-bank": "world-bank", "clean-air-fund": "clean-air-fund", "delhi-bocw-board": "delhi-bocw-board", "moefcc-ncap": "moefcc"}
ROLESYS = {"public": "accountability", "research": "evidence", "funder": "evidence", "multilateral": "reduce-emissions", "community": "protect-income; accountability", "ngo": "accountability"}
for r in old:
    if r.get("slug"): continue
    cat = CAT[r["org_id"]]
    r.update(slug=r["org_id"], category=cat, primary_type=r["sector"], legal_form="", profit_status="public" if cat == "public" else ("multilateral" if cat == "multilateral" else "nonprofit"),
             hq_country="india" if r["org_id"] not in ("world-bank", "clean-air-fund", "anti-slavery") else "global",
             countries_active="india", places=r["location"], domains="", communities=r["communities_served"], system_roles=ROLESYS[cat],
             summary=r["specific_activity_verified"], why_it_matters="", website="", record_status=r["status_at_cutoff"], activity_period="",
             last_public_activity="", date_last_checked="2026-11-22", source_class=r["evidence_quality"], business_role="", independent_test="",
             conflict_note="", funder_id=FUNDER.get(r["org_id"], ""), aliases="", claim_ids="", record_origin="baseline 2026-11-22")
extra = {"mht": ["caf_mht23"], "cse": ["caf_cse"], "teri": ["caf_teri"], "iit-kanpur": ["caf_iitk"], "hcwh": ["caf_hcwh"], "wri-india": ["caf_wri"],
         "clean-air-fund": ["caf_jkt", "caf_2021"], "world-bank": []}
for r in old:
    add = [cl[k] for k in extra.get(r["org_id"], [])]
    r["claim_ids"] = ";".join([x for x in r["claim_ids"].split(";") if x] + add)
ids = {r["org_id"] for r in old}
rows = old + [o for o in NEW if o["org_id"] not in ids]
write("organisations.csv", rows, base_cols + NEW_COLS)
PF = ["project_id", "title", "short_plain_language_description", "intervention_ids", "domain", "country", "specific_location", "airshed", "start_date", "end_date",
      "status", "target_groups", "intended_change", "activities", "outputs_reported", "outcomes_measured", "evaluation_type", "air_quality_objective",
      "cost_amount", "cost_currency", "cost_type", "continuing_cost_owner", "funding_visibility", "limitations", "claim_ids", "source_ids"]
write("projects.csv", PROJ, PF)
write("organisation-project-roles.csv", ROLES, ["organisation_id", "project_id", "role", "role_description", "source_ids", "verification_status"])
write("funding-flows.csv", FLOWS, list(FLOWS[0].keys()))
write("org-candidates.csv", [dict(candidate=a, country=b, type=c_, decision=d, reason=e, lead_url=f, reviewed=CHECKED) for a, b, c_, d, e, f in CAND],
      ["candidate", "country", "type", "decision", "reason", "lead_url", "reviewed"])
# P16: the GEF record is now read
pp = os.path.join(D, "programmes.csv"); P = list(csv.DictReader(open(pp, encoding="utf-8"))); pf = list(P[0].keys())
for p in P:
    if p["programme_id"] == "P16":
        p["source_ids"] = ";".join(x for x in [p["source_ids"], src["gef10609"], src["sunstar"]] if x)
        p["claim_ids"] = ";".join(x for x in [p["claim_ids"], cl["gef_emob"], cl["emob_cons"]] if x)
        p["amount"], p["currency"], p["amount_type"], p["nominal_year"] = "3788990", "USD", "approved (GEF grant)", "2022"
        p["relationship_verification"] = "verified: GEF project record (read 2026-11-23); consortium from press report"
        p["implementer"] = "UNIDO (GEF implementing agency); DTI (executing agency); consortium: Clean Air Asia, DLSU, EVAP, UEMI"
        p["notes"] = (p["notes"] + " | Upgraded 2026-11-23: GEF ID 10609 record read; co-financing US$77,477,969 not added to amount").strip(" |")
write("programmes.csv", P, pf)
print(f"sources now {len(list(csv.DictReader(open(reg.SRC))))}, claims {len(claim_rows()) if _rows else len(list(csv.DictReader(open(reg.CLM))))}, "
      f"orgs {len(rows)}, projects {len(PROJ)}, roles {len(ROLES)}, flows {len(FLOWS)}, candidates {len(CAND)}")

# Appended after the first run (2026-11-23): roles linking baseline organisations to their existing programme
# records, using each programme's own source_ids. Added directly to organisation-project-roles.csv:
#   delhi-bocw-board→P18 (public duty holder); moefcc-ncap→P19 (grantmaker, public budget);
#   world-bank→P01, P02, P04 (lender); gef→P16 (grantmaker); construction-unions→P18 (delivery partner, S016;S018).
