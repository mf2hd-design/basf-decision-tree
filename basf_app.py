import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="BASF Brand Architecture Tool",
    page_icon="🔵",
    layout="centered"
)

# --- Data for Guided Demo Mode (v4) ---
# Updated to include the new Stage 2 for relevant brands
DEMO_DATA = {
    "chemicals": {
        'stage1': {'index': 0, 'rationale': "The Chemicals division sells products to external customers."},
        'stage2': {'index': 0, 'rationale': "There are no specific legal or contractual requirements that override the standard process for this core business."},
        'stage3': {'index': 0, 'rationale': "This is the core business and carries a standard risk profile."},
        'stage4': {'index': 0, 'rationale': "The division is a wholly-owned and created part of BASF."},
        'stage5': {
            'rationale': "As the core of BASF's strategy, it scores high on contribution. As the masterbrand itself, it has no need for market distinction.",
            'score_A_checks': [True, True, False, True, True], 'score_B_checks': [False, False, False, False, False]
        }
    },
    "xarvio": {
        'stage1': {'index': 0, 'rationale': "Xarvio is a commercial digital solution sold to farmers."},
        'stage2': {'index': 0, 'rationale': "There are no overriding legal requirements for this internally developed brand."},
        'stage3': {'index': 0, 'rationale': "As a digital product, it does not carry an above-average reputational risk."},
        'stage4': {'index': 0, 'rationale': "Xarvio was developed internally, making it a wholly-owned BASF brand."},
        'stage5': {
            'rationale': "Xarvio is a strategic growth driver needing its own brand to compete with agile tech players and overcome a 'big corporate' headwind.",
            'score_A_checks': [False, False, True, True, True], 'score_B_checks': [True, True, True, True, True]
        }
    },
    "basf sonatrach propanchem": {
        'stage1': {'index': 0, 'rationale': "This is a commercial business that sells products externally."},
        'stage2': {'index': 1, 'rationale': "As a Joint Venture, the branding is explicitly defined in the legal agreement that formed the company. This agreement must be followed."}
    },
    "stoneville": {
        'stage1': {'index': 0, 'rationale': "Stoneville is a commercial brand of seeds sold to farmers."},
        'stage2': {'index': 0, 'rationale': "While acquired, we assume no specific legal constraints on branding beyond standard trademark law."},
        'stage3': {'index': 0, 'rationale': "Its risks are standard for the agriculture industry."},
        'stage4': {'index': 2, 'rationale': "Stoneville was acquired from Bayer, so it has significant pre-existing brand equity."},
        'stage4.1': {'index': 0, 'rationale': "Stoneville has a strong, positive reputation in its market that we want to retain."}
    },
    "insight 360": {
        'stage1': {'index': 1, 'rationale': "This is a tool for internal employees, so it's not a public-facing brand."}
    },
}

# --- Initialize Session State ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'entity_name' not in st.session_state:
    st.session_state.entity_name = ""
if 'scores' not in st.session_state:
    st.session_state.scores = {'A': 0, 'B': 0}
if 'demo_key' not in st.session_state:
    st.session_state.demo_key = None

# --- Functions ---
def start_evaluation(entity_name):
    st.session_state.entity_name = entity_name
    demo_key_check = entity_name.lower().strip().replace('°', '')
    if demo_key_check in DEMO_DATA:
        st.session_state.demo_key = demo_key_check
    set_stage(1)

def set_stage(stage_num):
    st.session_state.stage = stage_num
    st.rerun()

def reset_app():
    st.session_state.stage = 0
    st.session_state.scores = {'A': 0, 'B': 0}
    st.session_state.demo_key = None
    st.rerun()

def display_recommendation(recommendation, rationale, examples):
    st.success(f"**Recommendation: {recommendation}**")
    st.markdown("---")
    st.markdown(f"**Rationale:** {rationale}")
    if examples:
        st.markdown(f"**Similar Examples:** *{examples}*")
    st.markdown("---")
    if st.button("Evaluate Another Entity"):
        reset_app()

# --- Main App Logic ---

# STAGE 0: Welcome Screen
if st.session_state.stage == 0:
    st.title("BASF Brand Architecture Decision Tool")
    st.markdown("This interactive tool helps determine the appropriate branding and endorsement level for any entity within the BASF ecosystem.")
    
    st.subheader("Evaluate a New Entity")
    entity_name_input = st.text_input("Enter the name of a brand or entity to evaluate:", key="entity_name_input", label_visibility="collapsed")
    
    if st.button("Start Manual Evaluation"):
        if entity_name_input:
            start_evaluation(entity_name_input)
        else:
            st.warning("Please enter an entity name to begin.")
            
    st.markdown("---")
    st.subheader("Or, start a guided demo for a known brand:")
    
    demo_brands = ["Chemicals", "Xarvio", "Stoneville", "BASF SONATRACH PropanChem", "Insight 360"]
    cols = st.columns(len(demo_brands))
    for i, brand_key in enumerate(demo_brands):
        display_name = brand_key.replace("basf sonatrach propanchem", "BASF Sonatrach").title()
        with cols[i]:
            if st.button(display_name, key=brand_key, use_container_width=True):
                start_evaluation(display_name)

# STAGES 1, 2, 3, 4: The Filter Stages
elif st.session_state.stage in [1, 2, 3, 4, 4.1]:
    st.header(f"Evaluating: *{st.session_state.entity_name}*")
    
    stage_config = {
        1: {"header": "Stage 1: The Gatekeeper", "question": "What is its fundamental nature?", "options": ["A commercial offering", "An internal-facing tool", "A temporary communication initiative"], "next_stages": [2, 99, 98]},
        2: {"header": "Stage 2: Mandatory Directives", "question": "Is the branding dictated by a pre-existing legal or contractual requirement?", "options": ["No", "Yes"], "next_stages": [3, 97]},
        3: {"header": "Stage 3: Risk Assessment", "question": "Does it carry a significant, above-average reputational risk?", "options": ["No", "Yes"], "next_stages": [4, 96]},
        4: {"header": "Stage 4: The Structural Sorter", "question": "What is its ownership structure?", "options": ["A wholly-owned BASF business", "A Joint Venture", "A newly acquired company"], "next_stages": [5, 95, 4.1]},
        4.1: {"header": "Stage 4.1: Acquisition Evaluation", "question": "Does the acquired brand have significant negative equity?", "options": ["No", "Yes"], "next_stages": [94, 93]}
    }
    
    current_config = stage_config[st.session_state.stage]
    st.subheader(current_config["header"])
    
    demo_path_data = DEMO_DATA.get(st.session_state.demo_key, {})
    stage_key = f"stage{st.session_state.stage}"
    recommended_index = demo_path_data.get(stage_key, {}).get('index')
    
    def format_options(options, index):
        if index is None: return options
        formatted = options.copy()
        formatted[index] = f"**{formatted[index]}**"
        return formatted

    s_choice = st.radio(current_config["question"], format_options(current_config["options"], recommended_index), index=recommended_index, key=f"s{st.session_state.stage}_radio")
    
    if recommended_index is not None:
        st.info(f"**Demo Guidance:** {demo_path_data[stage_key]['rationale']}")

    if st.button("Proceed", type="primary"):
        selected_index = current_config["options"].index(s_choice.strip('*'))
        set_stage(current_config["next_stages"][selected_index])

# STAGE 5: DECISION ENGINE
elif st.session_state.stage == 5:
    st.header(f"Evaluating: *{st.session_state.entity_name}*")
    st.subheader("Stage 5: The Decision Engine")
    
    demo_path_data = DEMO_DATA.get(st.session_state.demo_key, {})
    stage5_data = demo_path_data.get('stage5', {})
    rec_checks_A = stage5_data.get('score_A_checks', [False]*5)
    rec_checks_B = stage5_data.get('score_B_checks', [False]*5)

    st.markdown("Check all that apply for each category.")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Part A: Strategic Contribution Score**")
        a1 = st.checkbox('Is it part of a designated "Core" business segment?', value=rec_checks_A[0])
        a2 = st.checkbox('Is it a cornerstone brand for the "Winning Ways" strategy?', value=rec_checks_A[1])
        a3 = st.checkbox('Is it part of a designated "Standalone" growth pillar?', value=rec_checks_A[2])
        a4 = st.checkbox('Does it directly deliver on a key corporate initiative?', value=rec_checks_A[3])
        a5 = st.checkbox('Does it strongly support the corporate purpose?', value=rec_checks_A[4])
        st.session_state.scores['A'] = sum([a1, a2, a3, a4, a5])
        st.write(f"**Score A: {st.session_state.scores['A']} / 5**")
    with col2:
        st.info("**Part B: Market Distinction Score**")
        b1 = st.checkbox('Does this brand need to appeal directly to an end-consumer (B2C / B2B2C)?', value=rec_checks_B[0])
        b2 = st.checkbox('Does it compete primarily with focused "pure players"?', value=rec_checks_B[1])
        b3 = st.checkbox('Is there a known negative perception of the BASF brand for this audience?', value=rec_checks_B[2])
        b4 = st.checkbox('Does it need clear differentiation from other BASF offerings?', value=rec_checks_B[3])
        b5 = st.checkbox('Does the business require a distinct, agile culture to succeed?', value=rec_checks_B[4])
        st.session_state.scores['B'] = sum([b1, b2, b3, b4, b5])
        st.write(f"**Score B: {st.session_state.scores['B']} / 5**")
        
    if st.session_state.demo_key and 'rationale' in stage5_data:
        st.info(f"**Demo Guidance:** {stage5_data['rationale']}")
        
    if st.button("Calculate Recommendation", type="primary"):
        set_stage(6)

# STAGE 6: FINAL RECOMMENDATION AND OTHER END STATES
elif st.session_state.stage >= 6:
    st.header(f"Result for: *{st.session_state.entity_name}*")
    
    if st.session_state.stage == 6:
        score_a = st.session_state.scores['A']
        score_b = st.session_state.scores['B']
        if score_a >= 3:
            if score_b <= 1: display_recommendation("BASF-Led", "The entity is a core expression of the BASF brand and benefits most from a direct connection.", "Chemicals, Care 360°")
            else: display_recommendation("BASF-Endorsed", "The entity is strategically vital but requires its own distinct brand to win in its specific market.", "Agriculture, Coatings, Xarvio")
        else:
            if score_b >= 2: display_recommendation("BASF-Endorsed (Lighter Touch)", "The entity is exploring a new space and needs its own brand to succeed.", "NewBiz")
            else: display_recommendation("Flag for Strategic Review", "The entity is not core to strategy and does not need its own brand to compete.", "A low-performing, undifferentiated legacy product.")
            
    elif st.session_state.stage == 99: display_recommendation("Descriptor / Internal Naming", "This is an internal-facing tool, not a public brand.", "Insight 360")
    elif st.session_state.stage == 98: display_recommendation("Descriptor / Internal Naming", "This is a temporary communication initiative, not a permanent brand.", "Anniversaries")
    elif st.session_state.stage == 97: display_recommendation("Follow Legal Directive", "The branding for this entity is pre-determined by a binding legal or contractual agreement which must be followed.", "BASF SONATRACH PropanChem")
    elif st.session_state.stage == 96: display_recommendation("Distanced Brand Strategy", "The entity carries significant reputational risk and must be strategically distanced from the masterbrand.", "A high-risk product in a controversial market.")
    elif st.session_state.stage == 95: display_recommendation("Strategically Aligned (Phased Approach)", "As a Joint Venture, the branding is subject to legal agreements and a unique co-branding strategy.", None) # JVs now go to 97
    elif st.session_state.stage == 94: display_recommendation("Strategically Aligned (Phased Approach)", "As a valuable acquisition with existing equity, the brand integration must be managed with a market-by-market plan to retain value.", "Stoneville, NewCo")
    elif st.session_state.stage == 93: display_recommendation("Retire Brand / Rebrand", "The acquired brand's baggage is a liability. This triggers a process to sunset the name and transition customers.", "A competitor with a poor environmental or safety record.")
