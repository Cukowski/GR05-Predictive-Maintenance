"""Build editable V6 milestone slides, offline PDF, and speaker notes.

Milestone date is 19 November per lecturer slide 9; 12 November is progress/preparation. Presenter assignments remain proposals.
Requires optional requirements-presentation.txt; data is read from verified exports.
"""
from pathlib import Path
import json,textwrap,base64,io,math
from PIL import Image,ImageDraw,ImageFont
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'presentations/milestone';ASSETS=OUT/'assets';ASSETS.mkdir(parents=True,exist_ok=True)
i=json.loads((ROOT/'reports/results/task5/training_insights.json').read_text())
m=json.loads((ROOT/'reports/results/task4/manifest.json').read_text())
S='Selçuk Ata Aksoy';D='Denzel Gregory Pragassa'
SOURCES={
 'course':'Supplied Project Tasks V6.0, pp. 1–2 (9 Nov 2026); milestone comments handout.',
 'dataset':'Arias Chao et al. (2021), Data 6(1), 5. https://doi.org/10.3390/data6010005',
 'task3':'Task 3 executed notebook + reports/results/task3_summary.json; figures generated from local DS01/DS02.',
 'task4':'Task 4 manifest: '+m['version_id']+'; docs/06-data-preparation.md.',
 'task5':'Executed Task 5 notebook; reports/results/task5/training_insights.json and accompanying CSV exports.',
 'linear':'https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares (accessed 11 Nov 2026).',
 'forest':'https://scikit-learn.org/stable/modules/ensemble.html#forest (accessed 11 Nov 2026).',
 'metrics':'https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics (accessed 11 Nov 2026).',
}
# Decode already executed Task 3/4 figures for the slide artifact; no re-analysis.
for filename,prefix in [('01-data-understanding.ipynb','task3'),('02-preprocessing.ipynb','task4')]:
 nb=json.loads((ROOT/'notebooks'/filename).read_text());count=0
 for cell in nb['cells']:
  for out in cell.get('outputs',[]):
   if 'image/png' in out.get('data',{}):
    (ASSETS/f'{prefix}-{count}.png').write_bytes(base64.b64decode(''.join(out['data']['image/png'])))
    count+=1
# Visual draft roadmap: future dates are team targets, not lecturer deadlines.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
roadmap=[('Business & definitions (review pending)','2026-10-15','2026-11-11',False),
         ('Data understanding','2026-10-22','2026-10-29',False),
         ('Preparation version','2026-10-29','2026-10-30',False),
         ('Descriptive analysis','2026-11-05','2026-11-11',False),
         ('Baseline + regression (proposed)','2026-11-20','2026-12-03',True),
         ('Grouped evaluation (proposed)','2026-12-04','2027-01-07',True),
         ('Final synthesis (proposed)','2027-01-08','2027-01-21',True)]
fig,ax=plt.subplots(figsize=(11,4.6))
for j,(label,start,end,planned) in enumerate(roadmap):
    a=mdates.date2num(datetime.fromisoformat(start));b=mdates.date2num(datetime.fromisoformat(end))
    ax.barh(j,b-a,left=a,color='#c3441f' if planned else '#386757',alpha=.7 if planned else 1)
ax.set_yticks(range(len(roadmap)),[r[0] for r in roadmap]);ax.invert_yaxis()
ax.xaxis_date();ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2));ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.axvline(mdates.date2num(datetime(2026,11,12)),color='#1e2926',ls='--',lw=1)
ax.axvline(mdates.date2num(datetime(2026,11,19)),color='#c3441f',ls='--',lw=1)
ax.set_title('12 Nov progress · 19 Nov milestone · future work dates proposed')
ax.spines[['top','right']].set_visible(False);fig.tight_layout()
fig.savefig(ASSETS/'roadmap.png',dpi=170);plt.close(fig)
slides=[]
def add(section,title,bullets,notes,presenter=S,source='course',figure=None,dark=False):
 slides.append(dict(section=section,title=title,bullets=bullets,notes=notes,presenter=presenter,source=source,figure=figure,dark=dark))
add('INTRODUCTION','Every cycle tells a story.',[
 'GR05 · Predictive Maintenance', 'Aircraft engine Remaining Useful Life',
 'Selçuk Ata Aksoy · Denzel Gregory Pragassa', 'HFU · Industrial Analytics · WS 2026/27'],
 'Opening: We study whether operating and sensor data can estimate how many flight cycles remain before simulated end-of-life. Today we present business understanding, data, preparation and descriptive findings. We have not trained an RUL model. The progress/preparation session is 12 November. The milestone presentation is Thursday 19 November, as stated on lecturer overview slide 9. Confirm class time and allowed speaking duration separately.',dark=True)
add('INTRODUCTION','Our question and scope',[
 'Can simple regression estimate RUL better than a transparent baseline?',
 'Prediction point: end of each completed flight.',
 'Scope: local DS01 + DS02; offline simulated-data study.',
 'Deliverable now: explainable evidence and prepared inputs.'],
 'RUL means remaining flight cycles, not a binary failure alarm. The full fleet history is available retrospectively, but predictor construction uses current and earlier flights only. We aim for a manageable two-student comparison; deep learning and deployment are outside initial scope.')
add('PROJECT PLAN','From question to evidence',[
 'October: Tasks 1–4 → definition, business, understanding, preparation.',
 '5–11 Nov: Task 5 → descriptive analysis, review and completion.',
 '12 Nov: progress/preparation; 19 Nov: milestone presentation.',
 'Next: baseline → regressors → grouped evaluation → 21 Jan final.'],
 'Walk the audience through the timeline without claiming the historical schedule was met on every date. The lecturer overview explicitly dates the milestone 19 November; the preceding week is preparation. Final 21 January is from the existing project plan; dates after the milestone are team targets, not new lecturer deadlines.')
add('DELIVERABLES','What exists and what comes next',[
 'Executed notebooks: understanding, preparation, descriptive analysis.',
 'Versioned local inputs, fitted preprocessing, audit CSVs and charts.',
 'Reports and local static pages: findings, preparation, analysis dashboard.',
 'Pending: human review, model training, MAE/RMSE and business evaluation.'],
 'Name the concrete artifacts and distinguish saved preprocessing from a trained predictive model. A clean, finite input matrix does not imply accurate forecasts. The deck itself is an AI-assisted draft requiring team review.',source='task4')
# Ten theory slides, as recommended by the separate presentation comments.
add('THEORY 01 / 10','Why maintenance planning is uncertain',[
 'Equipment condition changes during operation.',
 'Planners balance intervention lead time against continued operation.',
 'Sensor records can inform that decision, but uncertainty remains.'],
 'This frames the business problem qualitatively. We do not have observed repair costs or verified savings. Explain that maintenance planning uses several inputs; an RUL estimate would be one supporting signal, not a standalone safety decision.',source='dataset')
add('THEORY 02 / 10','Three maintenance strategies',[
 'Reactive: act after a fault or failure is detected.',
 'Preventive: intervene at scheduled intervals.',
 'Predictive: use condition/history to estimate future needs.'],
 'Use an everyday machinery example to explain the contrast. These are conceptual categories, not a claim that one strategy is always cheapest or safest. Our offline research explores the predictive component; it does not replace approved maintenance schedules.')
add('THEORY 03 / 10','Degradation is a process',[
 'A history records evolving condition rather than isolated failures.',
 'Different engines can have different initial health and lifetimes.',
 'Operating profiles can affect the signals we observe.'],
 'The supplied preprint describes simulated degradation with engine-to-engine variability. Avoid implying that a raw sensor signal maps uniquely to wear. The dataset gives run-to-failure histories, allowing retrospective labels.',source='dataset')
add('THEORY 04 / 10','Condition monitoring: what is observed?',[
 'Flight context: altitude, speed, throttle and inlet temperature.',
 'Response: temperatures, pressures, shaft speeds and fuel flow.',
 'Together they describe the engine operating under a mission.'],
 'Draw a simple input-to-response story: the flight puts demands on the engine, and sensor channels describe its response. Measured is the simulator channel label; the readings are not observed real engine failures.',source='dataset')
add('THEORY 05 / 10','Diagnosis and prognosis answer different questions',[
 'Diagnosis: what condition or fault may exist now?',
 'Prognosis: how might condition evolve, or how long remains?',
 'GR05 targets prognosis through continuous RUL regression.'],
 'The retrospective simulator health state can help explain data, but would give privileged information to a physical-sensor model. We exclude it from predictors. A health-class label is not the same as a numerical remaining-life estimate.')
add('THEORY 06 / 10','RUL is a countdown in flight cycles',[
 'Observed label: final cycle − current cycle.',
 'Example: final 100, current 30 → RUL 70 cycles.',
 'Final cycle is used to audit y, never supplied in X.'],
 'The example illustrates the convention, not a forecast. All engine-flight labels in Task 3 obeyed the countdown. Different engines have different final cycles, so cycle index alone is not a universal timer.',source='task3')
add('THEORY 07 / 10','A prediction needs a clock',[
 'At flight end: the current completed flight is known.',
 'Previous flights are known; future flights are not.',
 'Our summaries and rolling features respect that boundary.'],
 'Use the engine diary explanation. A centered rolling window or normalization by final lifetime would violate the boundary. A flight-end prediction contract is essential before selecting features or comparing models.',source='task4')
add('THEORY 08 / 10','The two directions of error matter',[
 'Optimistic RUL: estimates more remaining life than the label.',
 'Pessimistic RUL: estimates less remaining life than the label.',
 'Possible implications: delayed vs premature maintenance.'],
 'These are possible planning consequences, not observed costs. We will report error distributions and optimistic errors alongside average metrics. We have not designed a deployable intervention threshold.')
add('THEORY 09 / 10','CRISP-DM makes the work traceable',[
 'Business → data understanding → preparation.',
 'Modeling → evaluation → business implications.',
 'Each stage can send us back to improve an earlier decision.'],
 'Relate the course tasks to the process. A new variable definition or a leakage concern can require a new preparation version. We are at the descriptive milestone, moving toward modeling rather than claiming the whole lifecycle is finished.')
add('THEORY 10 / 10','Context shift challenges generalization',[
 'A signal can change with mission as well as degradation.',
 'DS02 development has class 3; test also has classes 1 and 2.',
 'A result on repeated flights may not generalize to unseen engines.'],
 'Explain domain shift using short versus long missions. This is a coverage observation, not a measured failure of a model. The small number of engine groups limits confidence and motivates group-aware evaluation.',source='task3')
# Five business-understanding slides.
add('BUSINESS 01 / 05','Who would use the output?',[
 'Maintenance planners: lead time and intervention timing.',
 'Reliability engineers: degradation patterns and error interpretation.',
 'Operations: downtime and premature-maintenance trade-offs.',
 'Our users today: students and lecturer reviewing evidence.'],
 'Distinguish hypothetical industrial stakeholders from actual project participants. We have not interviewed or deployed to an airline. Their interests frame the business case, while the academic users assess reproducibility and understanding.')
add('BUSINESS 02 / 05','The proposed value is decision support',[
 'Input: observed operating/sensor histories.',
 'Output later: an RUL estimate with documented error.',
 'Potential use: inform planning discussions.',
 'Value remains hypothetical until validated independently.'],
 'Explain that the dataset lacks actual economic outcomes. We cannot infer numerical savings from a temperature correlation. Do not present the work as an approved aircraft maintenance system.')
add('BUSINESS 03 / 05','How will success be assessed?',[
 'MAE: typical absolute error in flight cycles.',
 'RMSE: highlights larger cycle errors.',
 'Compare against constant training-RUL baselines.',
 'Also show per-engine and macro-average errors.'],
 'Define MAE as the average magnitude of error and RMSE as the square root of average squared error. Both remain in cycles. A mean constant is squared-error optimal; a median constant is absolute-error optimal. These are proposed comparisons, not results. Do not invent a numerical success threshold.',source='metrics')
add('BUSINESS 04 / 05','Make the scope feasible for two students',[
 'Start with simple baselines and classical regression.',
 'Use the 20-column baseline selection before 50 candidates.',
 'Evaluate on separate engine groups.',
 'No deep learning or live aircraft deployment in initial scope.'],
 'Task 4 integrated both collections with source identity and conservative grouping. A DS01-only refit is an appropriate sensitivity comparison later. Complexity should be justified by development-engine performance, not the desire to use more algorithms.',source='task4')
add('BUSINESS 05 / 05','Team responsibilities: proposed, not assumed',[
 'Selçuk: present data preparation and linear regression overview.',
 'Denzel: present descriptive findings and random forest overview.',
 'Both: review business claims, rehearse and understand all evidence.',
 'Confirm presenter allocation and individual contributions together.'],
 'This is a proposed speaking allocation for readiness, not an invented statement about who completed all implementation. Existing git evidence credits Denzel with the Task 5 draft; the log records AI-assisted completion. Individual grading means each student must understand and explain their algorithm and contributions.',presenter=D)
add('DATA SOURCE','Two local subsets, one lineage',[
 'NASA N-CMAPSS → Kaggle redistribution → local HDF5.',
 'DS01-005 and DS02-006; approximately 4.958 GiB combined.',
 '2020 local preprint differs from 2021 journal description.',
 'Current source labels recorded; original download-version match unproven.'],
 'Direct source link: https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation . Scientific reference: https://doi.org/10.3390/data6010005 . The paper declares CC0 for the dataset. Exact local hashes identify the files but do not verify upstream provenance. Raw files remain local.',source='dataset')
add('DATA 01 / 05','Reading → flight → engine history',[
 '14,159,058 ordered readings.',
 '1,542 dataset-engine-flight pairs.',
 '19 dataset-scoped source histories.',
 'Across-subset independence is not established.'],
 'Say nineteen source histories rather than nineteen proven independent engines. Shared IDs are conservatively linked later. Many rows in a flight are not independent samples. Show a small raw row and a prepared flight row if asked.',source='task3')
add('DATA 02 / 05','47 stored fields have different roles',[
 'W 4 + X_s 14: physical channel candidates.',
 'X_v 14 + T 10: hidden or virtual simulator quantities.',
 'Y 1: target; A 4: metadata.',
 'Stored fields are not all legitimate predictors.'],
 'Task 4 selected 17 of the 18 physical channels: P2 was excluded while unresolved in the older local source. The journal now confirms its definition; the feature representation stays unchanged; the metadata refresh creates a new version. Hidden health state, RUL and final lifetime are excluded from model inputs.',source='task3')
add('DATA 03 / 05','A number can still be a category',[
 'Unit ID: nominal label, despite float64 storage.',
 'Flight class: ordered category (short / medium / long).',
 'RUL: discrete ratio count; absolute temperature: continuous ratio.',
 'Units and statistical meaning guide valid comparisons.'],
 'Use the lecturer Dataset Scales example. Engine 10 is not twice engine 5. RUL zero means no flight cycles remain under our verified convention. Altitude is treated relative to a datum; cycle is an ordered index. Avoid equating numeric dtype with ratio scale.',source='task3')
add('DATA 04 / 05','Quality checks passed—with limits',[
 'No NaN/inf in the full Task 3 numeric scan.',
 'RUL countdown and cycle logic checks passed.',
 'Adjacent and sampled exact-duplicate checks found zero.',
 'No proof of physical accuracy or all non-adjacent uniqueness.'],
 'Cover six dimensions verbally: conformity, completeness, uniqueness, accuracy, timeliness and consistency. Finite data is not automatically correct data. Static simulation without timestamps prevents a calendar-freshness or gap-free-clock claim. Outlier fences are flags, not deletion instructions.',source='task3')
add('DATA 05 / 05','Engine lifetimes differ',[
 'DS01 histories: 75–100 flight cycles.',
 'DS02 histories: 59–89 flight cycles.',
 'Longer missions create more readings, not more engines.'],
 'The structural chart includes supplied test histories for data description, not hypothesis selection. Distinguish flight-cycle lifetime from elapsed engine hours; there is no verified timestamp column in the local arrays.',source='task3',figure='reports/figures/task5/engine_lifetimes.png')
add('PREPARATION 01 / 03','From snapshots to one completed flight',[
 '17 channel means + 17 within-flight spreads + reading count.',
 '3 causal trailing means + 3 previous-flight differences.',
 '4 physical combinations; 45 numeric candidates.',
 'Physical units: m, K, kPa, kg/s, rpm.'],
 'Each feature is available by current flight end. Previous differences are missing on first observed flights; this is expected. Whole-flight means mix phases. Ratios of means are diagnostic candidates, not calibrated efficiencies.',source='task4',figure='presentations/milestone/assets/task4-2.png')
add('PREPARATION 02 / 03','Split first; learn transformations on training only',[
 '574 train · 343 validation · 543 provided test.',
 '82 DS02 unit-10 flights quarantined due to possible DS01 test link.',
 'Training medians + missing indicators; training standardization.',
 'No validation/test fitting; shared IDs grouped conservatively.'],
 'Training has seven source histories but six conservative unit-ID groups. Equal-ID linking mitigates a risk, not proof of total independence. The imputer handles 57 expected first-difference gaps across all histories. Source DS01/DS02 becomes two one-hot columns.',source='task4',figure='presentations/milestone/assets/task4-0.png')
add('PREPARATION 03 / 03','Raw and prepared are both available locally',[
 'Raw HDF5: immutable originals, excluded from Git.',
 'Prepared CSVs: X inputs, y RUL, matching row identities.',
 '50-column candidate matrices; 20-column baseline option.',
 'Hashes, config, code and package versions identify the version.'],
 'Live-demo the current manifest and one prepared row, not a new 5 GB processing run. Dataset path comes from reports/results/task4/manifest.json. Saved preprocessor.joblib is a fitted transformer, not a predictive model. On GitHub Pages, raw/processed data are intentionally not public.',source='task4')
add('DESCRIPTIVE 01 / 05','The hypothesis-building sample',[
 f"{i['training_flights']} flights · {i['source_histories']} source histories · {i['conservative_groups']} conservative groups.",
 f"Training RUL: {i['rul_min']}–{i['rul_max']} cycles; mean {i['rul_mean']:.2f}.",
 'No test/quarantine sensor hypotheses.',
 'Validation is a descriptive check already seen in review.'],
 'The notebook now uses tracked reconstructed means by default and labels provenance. It also supports the hash-verified full Task 4 table. We do not claim a blinded preregistered confirmation because validation was already inspected.',presenter=D,source='task5',figure='reports/figures/task5/01_train_rul_histogram.png')
add('DESCRIPTIVE 02 / 05','T48 is consistently associated with RUL',[
 f"Within-history Pearson r: {i['t48_r_min']:.3f} to {i['t48_r_max']:.3f}.",
 'Negative in all 7 training source histories.',
 'Higher temperature tends to accompany lower historical RUL.',
 'Not a causal effect or prediction-accuracy result.'],
 'Explain the negative sign: as RUL counts down, temperature tends to be higher. The magnitude differs across histories and a scatter/time trajectory includes mission variation. No p-values assuming independent flights are reported.',presenter=D,source='task5',figure='reports/figures/task5/02_sensor_trajectories.png')
add('DESCRIPTIVE 03 / 05','Historical stage groups tell a clear story',[
 'Late 0–20 · Middle 21–50 · Early >50 cycles.',
 f"Paired late−early engine-median T48: +{i['late_minus_early_T48_K_median']:.2f} K median.",
 f"Range {i['late_minus_early_T48_K_min']:.2f}–{i['late_minus_early_T48_K_max']:.2f} K across 7 histories.",
 'Groups require true RUL; never use them as prediction inputs.'],
 'These are descriptive engine medians, not independent physical-engine treatment effects. The boxplot summarizes engine-stage medians; the separate condition plots are flight-weighted. Confounding remains possible. Grouping satisfies segmentation without claiming clustering.',presenter=D,source='task5',figure='reports/figures/task5/04_life_stage_sensor_boxplots.png')
add('DESCRIPTIVE 04 / 05','Context and heterogeneity temper the conclusion',[
 'Nc–RUL correlations span −0.153 to +0.199.',
 'Operating-condition medians differ across RUL stages.',
 'Previous-flight changes show weak pooled linear associations.',
 'H2 added predictive value and H3 causal effects remain untested.'],
 'This is why the business story cannot be a universal temperature threshold. Changes can be noisy while long-term level is informative; only later grouped model validation can assess incremental predictive value. Do not describe H1–H4 as formally statistically validated.',presenter=D,source='task5',figure='reports/figures/task5/05_operating_conditions.png')
add('DESCRIPTIVE 05 / 05','Observation → interpretation → next decision',[
 'Observe: late-life T48 is higher in this historical sample.',
 'Interpret: temperature and mission context merit investigation.',
 'Decide next: compare baseline and simple regressors on held-out engines.',
 'Do not infer savings or maintenance actions from correlation alone.'],
 'This is the required data-storytelling slide. In one minute: there is a repeatable descriptive signal; context and tiny group counts limit the inference; our next step is testable baseline-versus-regression evaluation. No model claim is hidden inside the story.',presenter=D,source='task5',dark=True)
add('ALGORITHM / SELÇUK','Linear regression: a transparent starting model',[
 'Predict RUL as an intercept plus weighted input features.',
 'Fit weights from training examples.',
 'Good first comparison: simple, inspectable coefficients.',
 'Proposed for next stage; not yet trained.'],
 'Proposed presenter: Selçuk. Explain a weighted sum using temperature and operating context as inputs. Coefficients are associations conditional on the other inputs, not causal effects. Regularization such as Ridge can be considered if correlated features make coefficients unstable. Do not claim fitted weights or accuracy.',source='linear')
add('ALGORITHM / SELÇUK','How we will check the linear model',[
 'Start with 20 baseline columns and constant mean/median references.',
 'Use development-engine validation; fit preparation in each fold.',
 'Report MAE/RMSE, per-engine errors and optimistic RUL.',
 'Check extrapolation, correlated predictors and residual patterns.'],
 'This is an experimental plan. A linear predictor may produce implausible negative RUL, so any clipping policy must be defined consistently and disclosed. Do not tune repeatedly to final test. Scalar errors should be shown in flight cycles.',source='linear')
add('ALGORITHM / DENZEL','Random forest regression: average many trees',[
 'Trees split feature space into rule-based regions.',
 'Average predictions across randomized trees.',
 'Candidate for nonlinear relations and interactions.',
 'Proposed comparison, not an established improvement.'],
 'Proposed presenter: Denzel. Explain one conceptual tree with an illustrative temperature/condition split, then the forest average. The example is not a fitted rule. Tree ensembles can fit source-specific patterns; the small number of engine groups is a serious constraint.',presenter=D,source='forest')
add('ALGORITHM / DENZEL','Keep the forest comparison modest',[
 'Predeclare a small depth/leaf-size search on development groups.',
 'Compare identical targets, splits and metrics with the baseline.',
 'Watch overfitting, collection effects and limited extrapolation.',
 'Feature importance would not prove causality.'],
 'Keep tuning small and reproducible. More trees do not create more independent training engines. Random forests generally interpolate within observed target patterns; operating shift remains important. Compare a DS01-only refit as a sensitivity case if time permits.',presenter=D,source='forest')
add('NEXT STEPS','The next decision is a fair model comparison',[
 '12 Nov progress; rehearse for the 19 Nov milestone.',
 'After milestone: constants + linear regression + random forest.',
 'Then: grouped validation, limitations, engine-wise errors.',
 'Final target: 21 January 2027, per existing course plan.'],
 'Suggested team targets: baseline implementation in the next project session, simple-model comparison by late November, robustness/error analysis during December, final narrative and presentation rehearsal in January. These are proposals, not lecturer-approved deadlines. Source/version and independence questions stay documented.')
add('READINESS / LIMITS','What we can defend—and what remains open',[
 'Verified: data structure, label logic, preparation and descriptive findings.',
 'Limits: small fleet, regime confounding, download-version match, cross-subset independence.',
 'Now confirmed: P2 is fan-inlet total pressure (journal Table 5).',
 'Unknown: predictive accuracy, real-world performance and cost savings.'],
 'P2 remains excluded from the selected representation. The metadata refresh creates a new version; earlier artifacts remain intact. Both students must review the draft and be able to explain every chart. Prepared artifacts are available locally; no external system has been deployed. Do not claim human approval or individual authorship not established by the team.',source='dataset')
add('SOURCES / QUESTIONS','Questions to carry into the next stage',[
 'Can the descriptive signal improve held-out-engine RUL estimates?',
 'How much is operating context versus degradation?',
 'Would a simpler DS01-only model be more defensible?',
 'Sources and AI assistance are documented in the repository.'],
 '\n'.join(SOURCES.values())+'\nAI disclosure: docs/ai-use-log.md. Notebook authorship/review caveats are in the Task 5 report. No full lecturer slides or raw datasets are embedded in this presentation.',presenter=D,source='dataset',dark=True)
slides[2]["figure"]="presentations/milestone/assets/roadmap.png"
assert len(slides)==40,len(slides)

# Visual system shared by PPTX and a portable, self-contained PDF.
W,H=1600,900;SCALE=120
PAPER='#eeede7';INK='#1e2926';MUTED='#58635d';LINE='#cdcec4';ACCENT='#c3441f';DARK='#111c19';LIGHT='#b9c4b4'
from matplotlib import font_manager
FONT=font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans'))
BOLD=font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans',weight='bold'))
prs=Presentation();prs.slide_width=Inches(13.333333);prs.slide_height=Inches(7.5)
rendered=[]

def rgb(hex):return RGBColor.from_string(hex.lstrip('#'))

def wrapping(text,size,width):
 font=ImageFont.truetype(FONT,size)
 lines=[]
 for raw in text.split('\n'):
  words=raw.split();line=''
  for word in words:
   candidate=(line+' '+word).strip()
   if line and font.getlength(candidate)>width:lines.append(line);line=word
   else:line=candidate
  lines.append(line)
 return '\n'.join(lines)

def fittext(slide,draw,text,x,y,w,h,size,color,bold=False):
 # Same manually wrapped lines in both formats; PPT has a generous bounding box.
 wrapped=wrapping(text,size,w)
 lines=wrapped.splitlines();lineheight=int(size*1.35)
 assert len(lines)*lineheight<=h+6,('Text too long',text[:50],len(lines),size,h)
 box=slide.shapes.add_textbox(Inches(x/SCALE),Inches(y/SCALE),Inches(w/SCALE),Inches(h/SCALE))
 tf=box.text_frame;tf.clear();tf.margin_left=tf.margin_right=0;tf.margin_top=tf.margin_bottom=0
 tf.word_wrap=False
 for j,line in enumerate(lines):
  para=tf.paragraphs[0] if j==0 else tf.add_paragraph();para.text=line
  para.font.name='DejaVu Sans';para.font.size=Pt(size*.6);para.font.bold=bold;para.font.color.rgb=rgb(color)
  para.space_after=Pt(size*.20)
 font=ImageFont.truetype(BOLD if bold else FONT,size)
 for j,line in enumerate(lines):draw.text((x,y+j*lineheight),line,font=font,fill=color)
 return len(lines)*lineheight

for n,s in enumerate(slides,1):
 slide=prs.slides.add_slide(prs.slide_layouts[6]);bg=DARK if s['dark'] else PAPER;fg=PAPER if s['dark'] else INK;muted=LIGHT if s['dark'] else MUTED
 slide.background.fill.solid();slide.background.fill.fore_color.rgb=rgb(bg)
 canvas=Image.new('RGB',(W,H),bg);draw=ImageDraw.Draw(canvas)
 fittext(slide,draw,'GR05 / INDUSTRIAL ANALYTICS',70,34,900,45,17,muted)
 fittext(slide,draw,s['section'],70,105,1400,45,18,'#ff8455' if s['dark'] else ACCENT)
 fittext(slide,draw,s['title'],70,164,1460,155,48,fg,True)
 if s['figure']:
  imagepath=ROOT/s['figure'];assert imagepath.exists(),imagepath
  im=Image.open(imagepath).convert('RGB');im.thumbnail((970,440))
  px=70+(970-im.width)//2;py=340+(440-im.height)//2
  canvas.paste(im,(px,py))
  slide.shapes.add_picture(str(imagepath),Inches(px/SCALE),Inches(py/SCALE),width=Inches(im.width/SCALE),height=Inches(im.height/SCALE))
  x,y,width=1090,340,430
  for bullet in s['bullets']:
   height=fittext(slide,draw,'• '+bullet,x,y,width,130,23,fg)
   y+=height+20
  assert y<815,('Chart bullets overflow',n,y)
 else:
  y=342
  for bullet in s['bullets']:
   height=fittext(slide,draw,'• '+bullet,90,y,1400,120,30 if s['dark'] else 28,fg)
   y+=height+24
  assert y<815,('Body overflow',n,y)
 # Compact readable footers meet lecturer's attribution and slide-number request.
 fittext(slide,draw,'Creators: GR05 (AI-assisted draft) | Presenter proposed: '+s['presenter'],70,824,1380,24,13,muted)
 fittext(slide,draw,f'{n:02d} / {len(slides):02d}',1430,824,110,24,15,muted)
 label='Evidence: '+SOURCES[s['source']]
 fittext(slide,draw,label,70,856,1460,35,10,muted)
 notes=f"Slide {n}: {s['title']}\nProposed presenter: {s['presenter']} (confirm with team).\n\n{s['notes']}\n\nEvidence: {SOURCES[s['source']]}\nDraft assembly: GR05 with documented AI assistance; team content review pending."
 slide.notes_slide.notes_text_frame.text=notes
 rendered.append(canvas)

prs.core_properties.title='GR05 — Predictive Maintenance: V6 milestone draft'
prs.core_properties.subject='Data understanding, preparation, descriptive findings and proposed algorithms; no model scores'
prs.core_properties.author='GR05 · AI-assisted draft; team review pending'
prs.save(OUT/'GR05-milestone-draft.pptx')
rendered[0].save(OUT/'GR05-milestone-draft.pdf',save_all=True,append_images=rendered[1:],resolution=150)
# Optional 20-slide route for a short slot; references/extended theory stay in full deck.
short=[1,2,3,4,6,10,15,17,20,21,22,24,26,27,29,30,31,33,34,36,38,39]
rendered[short[0]-1].save(OUT/'GR05-milestone-short-route.pdf',save_all=True,append_images=[rendered[n-1] for n in short[1:]],resolution=150)
# Contact sheet permits visual QA without a presentation application.
thumbs=[]
for n,im in enumerate(rendered,1):
 thumb=im.copy();thumb.thumbnail((400,225));thumbs.append(thumb)
contact=Image.new('RGB',(400*4,245*math.ceil(len(thumbs)/4)),'#d4d5cc')
for j,im in enumerate(thumbs):contact.paste(im,((j%4)*400,(j//4)*245))
contact.save(ASSETS/'contact-sheet.jpg',quality=88)
notes=['# GR05 milestone — speaker notes and rehearsal route',
       '\n**Progress/preparation session: 12 November 2026. Milestone presentation: Thursday 19 November 2026**, per lecturer overview slide 9. Confirm class time and allowed duration separately. Speaking allocations are proposals, not confirmed assignments. Full deck: 40 slides, including the theory depth suggested by the lecturer handout. Short route: '+', '.join(map(str,short))+'. The short route has 22 slides and reduces the separate handout\'s suggested theory/business slide counts; use it only if the allotted time requires it. The V6 topic coverage is retained.',
       '\nThe PDF is an offline rendering from the same slide specification; the PPTX is editable and has embedded notes. Open the PPTX once on the presentation machine to verify fonts/layout. The PDF provides a portable fallback.']
for n,s in enumerate(slides,1):
 notes.append(f"\n## Slide {n} — {s['title']}\n\nProposed presenter: {s['presenter']}.\n\n"+'\n'.join('- '+b for b in s['bullets'])+'\n\n'+s['notes']+'\n\nSource: '+SOURCES[s['source']])
(OUT/'speaker-notes.md').write_text('\n'.join(notes)+'\n')
(OUT/'slide-specification.json').write_text(json.dumps(slides,indent=2,ensure_ascii=False)+'\n')
print('Built 40-slide PPTX/PDF, 22-slide short-route PDF, notes and contact sheet.')
