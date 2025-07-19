import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="BASF Brand Compass",
    page_icon="🧭",
    layout="centered"
)

# --- Password Protection Logic (Robust Version) ---
def check_password():
    """Returns `True` if the user has the correct password."""
    def password_entered():
        if st.session_state.get("password") == "FFxBASF2025":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password" in st.session_state and not st.session_state.get("password_correct", False):
        st.error("😕 Password incorrect")
    return False

# --- Data Libraries ---
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
    "agriculture": {
        'stage1': {'index': 0, 'rationale': "The Agriculture division sells products to external customers."},
        'stage2': {'index': 0, 'rationale': "Its branding is not dictated by a specific legal requirement."},
        'stage3': {'index': 0, 'rationale': "Its risks are standard for the industry."},
        'stage4': {'index': 0, 'rationale': "This is a wholly-owned BASF business."},
        'stage5': {
            'rationale': "As a key growth pillar competing with pure-players, it is strategically vital but needs its own brand to win.",
            'score_A_checks': [False, True, True, True, False], 'score_B_checks': [True, True, False, True, False]
        }
    },
    "coatings": {
        'stage1': {'index': 0, 'rationale': "The Coatings division sells products to external customers."},
        'stage2': {'index': 0, 'rationale': "Its branding is not dictated by a specific legal requirement."},
        'stage3': {'index': 0, 'rationale': "Its risks are standard for the industry."},
        'stage4': {'index': 0, 'rationale': "This is a wholly-owned BASF business."},
        'stage5': {
            'rationale': "As a key growth pillar competing with pure-players, it is strategically vital but needs its own brand to win.",
            'score_A_checks': [False, True, True, True, False], 'score_B_checks': [True, True, False, True, False]
        }
    },
    "ecms": {
        'stage1': {'index': 0, 'rationale': "ECMS sells products to external customers."},
        'stage2': {'index': 0, 'rationale': "Its branding is not dictated by a specific legal requirement."},
        'stage3': {'index': 0, 'rationale': "Its risks are standard for the industry."},
        'stage4': {'index': 0, 'rationale': "This is a wholly-owned BASF business."},
        'stage5': {
            'rationale': "As a sustainability-focused growth pillar, it's highly strategic but needs a distinct identity for its specialized market.",
            'score_A_checks': [False, True, True, True, True], 'score_B_checks': [False, True, False, True, True]
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
    "care360": {
        'stage1': {'index': 0, 'rationale': "This is a platform of solutions offered to external customers."},
        'stage2': {'index': 0, 'rationale': "There are no overriding legal requirements."},
        'stage3': {'index': 0, 'rationale': "Its risk profile is standard."},
        'stage4': {'index': 0, 'rationale': "It is a wholly-owned strategic initiative developed by BASF."},
        'stage5': {
            'rationale': "As a solutions platform, its entire purpose is to showcase the power of the masterbrand. It needs to be the embodiment of BASF, not distinct from it.",
            'score_A_checks': [False, True, False, True, True], 'score_B_checks': [False, False, False, False, False]
        }
    },
    "newbiz": {
        'stage1': {'index': 0, 'rationale': "This is a commercial business that sells products externally."},
        'stage2': {'index': 0, 'rationale': "Its branding is not dictated by a specific legal requirement."},
        'stage3': {'index': 0, 'rationale': "Risk is standard for a new venture."},
        'stage4': {'index': 0, 'rationale': "This is a new, wholly-owned venture created by BASF."},
        'stage5': {
            'rationale': "This new venture is not yet core to strategy but needs high market distinction to succeed in a new field.",
            'score_A_checks': [False, False, False, True, False], 'score_B_checks': [True, True, True, True, True]
        }
    },
    "newco": {
        'stage1': {'index': 0, 'rationale': "This is a commercial business that sells products externally."},
        'stage2': {'index': 0, 'rationale': "We assume the M&A deal has no unusual branding constraints."},
        'stage3': {'index': 0, 'rationale': "Assuming this is a standard acquisition, the risk profile is not above-average."},
        'stage4': {'index': 2, 'rationale': "As a 'newly acquired company,' its existing brand equity must be handled carefully."},
        'stage4.1': {'index': 0, 'rationale': "We are assuming 'NewCo' is a valuable asset with positive brand equity."}
    },
    "basfsonatrachpropanchem": {
        'stage1': {'index': 0, 'rationale': "This is a commercial business that sells products externally."},
        'stage2': {'index': 1, 'rationale': "As a Joint Venture, the branding is explicitly defined in the legal agreement that formed the company. This agreement must be followed."}
    },
    "insight360": {
        'stage1': {'index': 1, 'rationale': "This is a tool for internal employees, so it's not a public-facing brand."}
    },
    "anniversaries": {
        'stage1': {'index': 2, 'rationale': "This is a temporary campaign led by BASF, not a permanent brand in the portfolio."}
    },
}

RESULT_DATA = {
    'basf_led': {'recommendation': "BASF-Led", 'rationale': "The entity is a core expression of the BASF brand and benefits most from a direct connection.", 'activation_text': "This means we don't create a separate brand. The entity is branded simply as 'BASF [Entity Name]'. It lives on the main BASF website and is sold by the BASF sales team, reinforcing the power and innovation of the masterbrand.", 'examples': "Chemicals, Care 360°"},
    'basf_endorsed': {'recommendation': "BASF-Endorsed", 'rationale': "The entity is strategically vital but requires its own distinct brand to win in its specific market.", 'activation_text': "This means the entity has its own distinct brand and identity. The endorsement, such as 'powered by BASF science,' is used strategically to provide the ultimate reason to believe—giving the brand both the unique story it needs and the scientific credibility customers trust.", 'examples': "Agriculture, Coatings, Xarvio"},
    'basf_associated': {'recommendation': "BASF-Associated", 'rationale': "The entity is exploring a new space and needs brand independence. A lighter, strategic association provides credibility without high commitment.", 'activation_text': "This means the entity has its own independent brand. The connection to BASF is lighter and more strategic, often used in communications rather than on packaging. This provides credibility without tying the venture too closely to the masterbrand's core identity.", 'examples': "NewBiz"},
    'flag_review': {'recommendation': "Flag for Strategic Review", 'rationale': "The entity is not core to strategy and does not need its own brand to compete.", 'activation_text': "This is not a branding recommendation but a business flag. The next step is a formal business review to determine its future in the portfolio.", 'examples': "A low-performing, undifferentiated legacy product."},
    'internal_naming': {'recommendation': "Descriptor / Internal Naming", 'rationale': "This is an internal-facing tool, not a public brand. The Compass's work is complete.", 'activation_text': "This entity does not require a public-facing brand. It should be named according to BASF's internal naming conventions for projects, tools, or initiatives.", 'examples': "Insight 360"},
    'comms_initiative': {'recommendation': "Descriptor / Internal Naming", 'rationale': "This is a temporary communication initiative, not a permanent brand. The Compass's work is complete.", 'activation_text': "This entity does not require a public-facing brand. It should be named according to BASF's internal naming conventions for projects, tools, or initiatives.", 'examples': "Anniversaries"},
    'legal_directive': {'recommendation': "Follow Legal Directive", 'rationale': "The branding for this entity is pre-determined by a binding legal or contractual agreement which must be followed. The Compass's work is complete.", 'activation_text': "The branding for this entity is dictated by a binding legal or contractual agreement. The primary action is to consult the specific legal documents (e.g., the Joint Venture agreement) and implement the branding exactly as specified.", 'examples': "BASF SONATRACH PropanChem"},
    'independent_risk': {'recommendation': "Independent (for risk insulation)", 'rationale': "The entity carries significant reputational risk and must be strategically independent and distanced from the masterbrand.", 'activation_text': "This means the entity must operate as a fully independent brand with no visible connection to BASF. This is a strategic decision to insulate the BASF masterbrand from any potential reputational risk associated with the entity.", 'examples': "A high-risk product in a controversial market."},
    'strategically_aligned': {'recommendation': "Strategically Aligned (Phased Approach)", 'rationale': "As a valuable acquisition or JV with existing equity, the brand integration must be managed with a market-by-market plan to retain value. The Compass's work is complete.", 'activation_text': "This triggers a market-by-market integration plan. The brand's relationship to BASF will vary by region, from 'Maintain & Reassure' (e.g., 'Stoneville, from BASF') where its equity is high, to 'Lead with BASF' where its equity is low. The goal is to maximize value in every market.", 'examples': "Stoneville, NewCo"},
    'retire_rebrand': {'recommendation': "Independent (Retire & Rebrand)", 'rationale': "The acquired brand's baggage is a liability. The recommendation is to make it independent by retiring the name and transitioning customers to a BASF brand.", 'activation_text': "This means the acquired brand identity will be retired. A formal plan must be created to migrate customers and assets to a new or existing BASF brand, thereby making the business independent of the problematic legacy name.", 'examples': "A competitor with a poor environmental or safety record."}
}

# --- Main App Function ---
def run_app():
    # Initialize Session State
    if 'stage' not in st.session_state: st.session_state.stage = 0
    if 'entity_name' not in st.session_state: st.session_state.entity_name = ""
    if 'scores' not in st.session_state: st.session_state.scores = {'A': 0, 'B': 0}
    if 'demo_key' not in st.session_state: st.session_state.demo_key = None

    # Functions
    def start_evaluation(entity_name):
        st.session_state.entity_name = entity_name
        # Normalize the key for matching
        demo_key_check = entity_name.lower().strip().replace('°', '').replace(' ', '')
        if demo_key_check in DEMO_DATA: st.session_state.demo_key = demo_key_check
        set_stage(1)

    def set_stage(stage_num):
        st.session_state.stage = stage_num
        st.rerun()

    def reset_app():
        # Clear all session state keys to ensure a clean start
        for key in list(st.session_state.keys()):
            if key != 'password_correct': del st.session_state[key]
        st.rerun()

    def display_result(result_key):
        result = RESULT_DATA[result_key]
        st.header("Result")
        st.write(f"**Entity Evaluated:** *{st.session_state.entity_name}*")
        st.markdown("---")
        st.subheader("Phase 3: Activation - The 'How'")
        st.caption("This final phase provides the actionable guide for execution. The recommendation below links to a specific Implementation Guide.")
        st.success(f"**Recommendation: {result['recommendation']}**")
        st.markdown(f"**Rationale:** {result['rationale']}")
        st.markdown("---")
        st.markdown(result['activation_text'])
        st.markdown(f"**Similar Examples:** *{result['examples']}*")
        st.markdown("---")
        if st.button("Evaluate Another Entity"): reset_app()
    
    # --- App Logic ---
    st.title("🧭 The BASF Brand Compass")
    if st.session_state.stage == 0:
        st.markdown("An interactive tool to provide clear, strategic direction for the BASF brand architecture.")
        st.markdown("""
        - **Phase 1: Qualification** - *Answers 'What is this entity and does it need a brand architecture decision?'*
        - **Phase 2: Classification** - *Answers 'Where does this brand fit within our brand architecture?'*
        - **Phase 3: Activation** - *Answers 'How do we bring this brand to life?'*
        """)
        st.subheader("Evaluate a New Entity")
        entity_name_input = st.text_input("Enter name:", key="entity_name_input", label_visibility="collapsed")
        if st.button("Start Manual Evaluation"):
            if entity_name_input: start_evaluation(entity_name_input)
            else: st.warning("Please enter an entity name to begin.")
        st.markdown("---")
        st.subheader("Or, start a guided demo for a known brand:")
        demo_brands = list(DEMO_DATA.keys())
        brand_display_names = {"basfsonatrachpropanchem": "BASF Sonatrach", "ecms": "ECMS", "newbiz": "NewBiz", "newco": "NewCo", "care360": "Care 360°"}
        cols = st.columns(4)
        for i, brand_key in enumerate(demo_brands):
            display_name = brand_display_names.get(brand_key, brand_key.title())
            with cols[i % 4]:
                if st.button(display_name, key=brand_key, use_container_width=True): start_evaluation(display_name)
    
    # Logic for all subsequent stages
    else:
        stage_config = {
            1: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Gatekeeper", "explanation": "This first step determines if the entity is a commercial brand requiring a strategic decision.", "question": "What is its fundamental nature?", "options": ["A commercial offering", "An internal-facing tool", "A temporary communication initiative"], "next_stages": [2, 101, 102]},
            2: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Mandatory Directives", "explanation": "This step checks for any non-negotiable legal or contractual obligations that pre-determine the branding approach.", "question": "Is branding dictated by a pre-existing legal or contractual requirement?", "options": ["No", "Yes"], "next_stages": [3, 103]},
            3: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Risk Assessment", "explanation": "This is a safety check to determine if the entity carries a significant reputational risk that could harm the masterbrand.", "question": "Does it carry a significant, above-average reputational risk?", "options": ["No", "Yes"], "next_stages": [4, 104]},
            4: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Structural Sorter", "explanation": "This step sorts entities based on their ownership, as special cases like Joint Ventures and Acquisitions have unique strategic needs.", "question": "What is its ownership structure?", "options": ["A wholly-owned BASF business", "A Joint Venture", "A newly acquired company"], "next_stages": [5, 105, 4.1]},
            4.1: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Acquisition Evaluation", "explanation": "For acquired brands, we must assess their existing reputation to decide whether to leverage their brand equity or retire it.", "question": "Does the acquired brand have significant negative equity?", "options": ["No", "Yes"], "next_stages": [106, 107]}
        }

        # If it's a filter stage
        if st.session_state.stage in stage_config:
            st.header(f"Evaluating: *{st.session_state.entity_name}*")
            current_config = stage_config[st.session_state.stage]
            st.subheader(current_config["phase_name"])
            st.write(f"**{current_config['header']}**")
            st.caption(current_config['explanation'])
            demo_path_data = DEMO_DATA.get(st.session_state.demo_key, {})
            stage_key = f"stage{st.session_state.stage}"
            recommended_index = demo_path_data.get(stage_key, {}).get('index')
            def format_options(options, index):
                if index is None: return options
                formatted = options.copy()
                formatted[index] = f"**{formatted[index]}**"
                return formatted
            s_choice = st.radio(current_config["question"], format_options(current_config["options"], recommended_index), index=recommended_index, key=f"s{st.session_state.stage}_radio", label_visibility="collapsed")
            if recommended_index is not None: st.info(f"**Demo Guidance:** {demo_path_data[stage_key]['rationale']}")
            if st.button("Proceed", type="primary"):
                selected_index = current_config["options"].index(s_choice.strip('*'))
                set_stage(current_config["next_stages"][selected_index])

        # If it's the scoring engine
        elif st.session_state.stage == 5:
            st.header(f"Evaluating: *{st.session_state.entity_name}*")
            st.subheader("Phase 2: Classification - The 'Where'")
            st.write("**The Strategic Core**")
            st.caption("This is the heart of the process. The scores from this scorecard provide a clear, data-driven recommendation for where the brand fits within our brand architecture.")
            demo_path_data = DEMO_DATA.get(st.session_state.demo_key, {})
            stage5_data = demo_path_data.get('stage5', {})
            rec_checks_A = stage5_data.get('score_A_checks', [False]*5)
            rec_checks_B = stage5_data.get('score_B_checks', [False]*5)
            st.markdown("---")
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
            st.markdown("---")
            if st.session_state.demo_key and 'rationale' in stage5_data: st.info(f"**Demo Guidance:** {stage5_data['rationale']}")
            if st.button("Calculate Recommendation", type="primary"): set_stage(6)
        
        # If it's any of the final recommendation pages
        else:
            result_key_map = {
                101: 'internal_naming', 102: 'comms_initiative', 103: 'legal_directive',
                104: 'independent_risk', 105: 'strategically_aligned', 106: 'strategically_aligned',
                107: 'retire_rebrand'
            }
            outcome_key = None
            if st.session_state.stage == 6:
                score_a = st.session_state.scores['A']
                score_b = st.session_state.scores['B']
                if score_a >= 3:
                    outcome_key = 'basf_led' if score_b <= 1 else 'basf_endorsed'
                else:
                    outcome_key = 'basf_associated' if score_b >= 2 else 'flag_review'
            else:
                outcome_key = result_key_map.get(st.session_state.stage)
            
            if outcome_key:
                result = RESULT_DATA[outcome_key]
                display_result(result)

# --- App Execution with Password Check ---
if check_password():
    run_app()
