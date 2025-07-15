import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="BASF Brand Architecture Tool",
    page_icon="🔵",
    layout="centered"
)

# --- Comprehensive Data for Guided Demo Mode ---
DEMO_DATA = {
    # Core Business Example
    "chemicals": {
        'stage1': {'index': 0, 'rationale': "The Chemicals division sells products to external customers."},
        'stage2': {'index': 0, 'rationale': "This is the core business and carries a standard risk profile."},
        'stage3': {'index': 0, 'rationale': "The division is a wholly-owned and created part of BASF."},
        'stage4': {
            'rationale': "As the core of BASF's strategy, it scores high on contribution. As the masterbrand itself, it has no need for market distinction.",
            'score_A_checks': [True, True, False, True, True], 'score_B_checks': [False, False, False, False, False]
        }
    },
    # Standalone Business Examples
    "agriculture": {
        'stage1': {'index': 0, 'rationale': "The Agriculture division sells products to external customers."},
        'stage2': {'index': 0, 'rationale': "Its risks are standard for the industry."},
        'stage3': {'index': 0, 'rationale': "This is a wholly-owned BASF business."},
        'stage4': {
            'rationale': "As a key growth pillar competing with pure-players, it is strategically vital but needs its own brand to win.",
            'score_A_checks': [False, True, True, True, False], 'score_B_checks': [True, True, False, True, False]
        }
    },
    "coatings": {
        'stage1': {'index': 0, 'rationale': "The Coatings division sells products to external customers."},
        'stage2': {'index': 0, 'rationale': "Its risks are standard for the industry."},
        'stage3': {'index': 0, 'rationale': "This is a wholly-owned BASF business."},
        'stage4': {
            'rationale': "As a key growth pillar competing with pure-players, it is strategically vital but needs its own brand to win.",
            'score_A_checks': [False, True, True, True, False], 'score_B_checks': [True, True, False, True, False]
        }
    },
    "ecms": {
        'stage1': {'index': 0, 'rationale': "ECMS sells products to external customers."},
        'stage2': {'index': 0, 'rationale': "Its risks are standard for the industry."},
        'stage3': {'index': 0, 'rationale': "This is a wholly-owned BASF business."},
        'stage4': {
            'rationale': "As a sustainability-focused growth pillar, it's highly strategic but needs a distinct identity for its specialized market.",
            'score_A_checks': [False, True, True, True, True], 'score_B_checks': [False, True, False, True, True]
        }
    },
    # Digital & Solution Examples
    "xarvio": {
        'stage1': {'index': 0, 'rationale': "Xarvio is a commercial digital solution sold to farmers."},
        'stage2': {'index': 0, 'rationale': "As a digital product, it does not carry an above-average reputational risk."},
        'stage3': {'index': 0, 'rationale': "Xarvio was developed internally, making it a wholly-owned BASF brand."},
        'stage4': {
            'rationale': "Xarvio is a strategic growth driver needing its own brand to compete with agile tech players and overcome a 'big corporate' headwind.",
            'score_A_checks': [False, False, True, True, True], 'score_B_checks': [True, True, True, True, True]
        }
    },
    "care 360": {
        'stage1': {'index': 0, 'rationale': "This is a platform of solutions offered to external customers."},
        'stage2': {'index': 0, 'rationale': "Its risk profile is standard."},
        'stage3': {'index': 0, 'rationale': "It is a wholly-owned strategic initiative developed by BASF."},
        'stage4': {
            'rationale': "As a solutions platform, its entire purpose is to showcase the power of the masterbrand. It needs to be the embodiment of BASF, not distinct from it.",
            'score_A_checks': [False, True, False, True, True], 'score_B_checks': [False, False, False, False, False]
        }
    },
    # New Business & M&A Examples
    "newbiz": {
        'stage1': {'index': 0, 'rationale': "This is a commercial business that sells products externally."},
        'stage2': {'index': 0, 'rationale': "Risk is standard for a new venture."},
        'stage3': {'index': 0, 'rationale': "This is a new, wholly-owned venture created by BASF."},
        'stage4': {
            'rationale': "This new venture is not yet core to strategy but needs high market distinction to succeed in a new field.",
            'score_A_checks': [False, False, False, True, False], 'score_B_checks': [True, True, True, True, True]
        }
    },
    "newco": {
        'stage1': {'index': 0, 'rationale': "This is a commercial business that sells products externally."},
        'stage2': {'index': 0, 'rationale': "Assuming this is a standard acquisition, the risk profile is not above-average."},
        'stage3': {'index': 2, 'rationale': "As a 'newly acquired company,' its existing brand equity must be handled carefully."},
        'stage3.1': {'index': 0, 'rationale': "We are assuming 'NewCo' is a valuable asset with positive brand equity."}
    },
    # JV & Non-Brand Examples
    "basf sonatrach propanchem": {
        'stage1': {'index': 0, 'rationale': "This is a commercial business that sells products externally."},
        'stage2': {'index': 0, 'rationale': "The risk profile is standard for a core chemicals business."},
        'stage3': {'index': 1, 'rationale': "This is a Joint Venture, which is a special legal structure requiring a bespoke brand strategy."}
    },
    "insight 360": {
        'stage1': {'index': 1, 'rationale': "This is a tool for internal employees, so it's not a public-facing brand."}
    },
    "anniversaries": {
        'stage1': {'index': 2, 'rationale': "This is a temporary campaign led by BASF, not a permanent brand in the portfolio."}
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
    
    demo_brands = list(DEMO_DATA.keys())
    cols = st.columns(4)
    for i, brand_key in enumerate(demo_brands):
        # Format the display name nicely
        display_name = brand_key.replace("basf sonatrach propanchem", "BASF Sonatrach").replace("ecms", "ECMS").replace("newbiz", "NewBiz").replace("newco", "NewCo").title()
        if st.button(display_name, key=brand_key, use_container_width=True):
            start_evaluation(display_name)

# STAGES 1, 2, 3: The Filter Stages
elif st.session_state.stage in [1, 2, 3, 3.1]:
    st.header(f"Evaluating: *{st.session_state.entity_name}*")
    
    stage_config = {
        1: {"header": "Stage 1: The Gatekeeper", "question": "What is its fundamental nature?", "options": ["A commercial offering", "An internal-facing tool", "A temporary communication initiative"], "next_stages": [2, 99, 98]},
        2: {"header": "Stage 2: The Risk Assessment", "question": "Does it carry a significant, above-average reputational risk?", "options": ["No", "Yes"], "next_stages": [3, 97]},
        3: {"header": "Stage 3: The Structural Sorter", "question": "What is its ownership structure?", "options": ["A wholly-owned BASF business", "A Joint Venture", "A newly acquired company"], "next_stages": [4, 96, 3.1]},
        3.1: {"header": "Stage 3.1: Acquisition Evaluation", "question": "Does the acquired brand have significant negative equity?", "options": ["No", "Yes"], "next_stages": [95, 94]}
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

# STAGE 4: DECISION ENGINE
elif st.session_state.stage == 4:
    st.header(f"Evaluating: *{st.session_state.entity_name}*")
    st.subheader("Stage 4: The Decision Engine")
    
    demo_path_data = DEMO_DATA.get(st.session_state.demo_key, {})
    stage4_data = demo_path_data.get('stage4', {})
    rec_checks_A = stage4_data.get('score_A_checks', [False]*5)
    rec_checks_B = stage4_data.get('score_B_checks', [False]*5)

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
        b1 = st.checkbox('Is the primary audience B2C or B2B2C?', value=rec_checks_B[0])
        b2 = st.checkbox('Does it compete primarily with focused "pure players"?', value=rec_checks_B[1])
        b3 = st.checkbox('Is there a known negative perception of the BASF brand for this audience?', value=rec_checks_B[2])
        b4 = st.checkbox('Does it need clear differentiation from other BASF offerings?', value=rec_checks_B[3])
        b5 = st.checkbox('Does the business require a distinct, agile culture to succeed?', value=rec_checks_B[4])
        st.session_state.scores['B'] = sum([b1, b2, b3, b4, b5])
        st.write(f"**Score B: {st.session_state.scores['B']} / 5**")
        
    if st.session_state.demo_key and 'rationale' in stage4_data:
        st.info(f"**Demo Guidance:** {stage4_data['rationale']}")
        
    if st.button("Calculate Recommendation", type="primary"):
        set_stage(5)

# STAGE 5: FINAL RECOMMENDATION AND OTHER END STATES
elif st.session_state.stage >= 5:
    st.header(f"Result for: *{st.session_state.entity_name}*")
    
    if st.session_state.stage == 5:
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
    elif st.session_state.stage == 97: display_recommendation("Distanced Brand Strategy", "The entity carries significant reputational risk and must be strategically distanced from the masterbrand.", "A high-risk product in a controversial market.")
    elif st.session_state.stage == 96: display_recommendation("Strategically Aligned (Phased Approach)", "As a Joint Venture, the branding is subject to legal agreements and a unique co-branding strategy.", "BASF SONATRACH PropanChem")
    elif st.session_state.stage == 95: display_recommendation("Strategically Aligned (Phased Approach)", "As a valuable acquisition with existing equity, the brand integration must be managed with a market-by-market plan to retain value.", "Stoneville, NewCo")
    elif st.session_state.stage == 94: display_recommendation("Retire Brand / Rebrand", "The acquired brand's baggage is a liability. This triggers a process to sunset the name and transition customers.", "A competitor with a poor environmental or safety record.")