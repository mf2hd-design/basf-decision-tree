import streamlit as st
import base64
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="BASF Brand Compass",
    page_icon="🧭",
    layout="centered"
)

# --- Password Protection Logic ---
def check_password():
    def password_entered():
        if st.session_state.get("password") == "FFxBASF2025":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.title("🧭 The BASF Brand Compass")
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    if "password" in st.session_state and not st.session_state.get("password_correct", False):
        st.error("😕 Password incorrect")
    return False

# --- Data Libraries (Fully Restored with All Guidance) ---
DEMO_DATA = {
    "chemicals": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 1,
                  'stage4': {'rationale': "As a wholly-owned business, it proceeds to the resource check."},
                  'stage5': {'rationale': "As the core engine of BASF, its contribution is maximum. Its entire value comes from being BASF, so its need for market distinction is minimal."}},
    "chemetall": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 0, 'negative_equity': 1,
                   'stage1.11': {'rationale': "We assume Chemetall has positive brand equity, so it proceeds to the scorecard."}},
    "ecms": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 1},
    "coatings": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 1},
    "newco": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 0, 'negative_equity': 1,
              'stage1.11': {'rationale': "This demo assumes a standard acquisition of a company with a valuable, positive brand equity that should be integrated."}},
    "basfsonatrachpropanchem": {'purpose': 0, 'nature': 0, 'ownership': 2, 'jv_equity': 0,
                                 'stage3': {'index': 0, 'rationale': "A legal directive already exists in the JV agreement, which must be followed. This would typically result in a specific outcome, but for the demo we proceed."}},
    "newbiz": {'purpose': 0, 'nature': 0},
    "care360": {'purpose': 0, 'nature': 0},
    "insight360": {'purpose': 1, 'audience': 0, 'stage0.6': {'rationale': "As an internal tool, it's non-commercial and directed at employees, leading to a 'BASF-Led' outcome."}},
    "anniversaries": {'purpose': 1, 'audience': 1, 'stage0.6': {'rationale': "As a temporary external campaign, it's non-commercial, leading to a 'BASF-Led' outcome."}},
    "glasurit": {'purpose': 0, 'nature': 1, 'governance': 1, 'dependencies': 1, 'resources_prod': 1,
                 'stage201': {'rationale': "The product is managed by a BASF-branded entity (Coatings), so it can proceed."},
                 'stage203': {'rationale': "It is a standalone product, not a feature of a larger offer, so it requires further evaluation."},
                 'stage204': {'rationale': "The brand has a dedicated budget, allowing it to be considered for an endorsed identity."}},
    "extractmax": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 1, 'risk': 0,
                   'stage2': {'rationale': "Operating in a controversial industry presents a significant reputational risk, triggering the 'Independent' off-ramp to protect the masterbrand."}},
    "oldcheminc": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 0, 'negative_equity': 0,
                   'stage1.11': {'rationale': "The acquired brand has a known negative reputation, which is a liability. This triggers the 'Retire & Rebrand' outcome."}},
    "polyweld800": {'purpose': 0, 'nature': 1},
    "noresourceproduct": {'purpose': 0, 'nature': 1, 'governance': 1, 'dependencies': 1, 'resources_prod': 0,
                         'stage204': {'rationale': "The product team does not have a dedicated budget to support a distinct brand, triggering the 'Flag for Review' outcome."}}
}


RESULT_DATA = {
    'basf_led': {'recommendation': "BASF-Led", 'rationale': "This entity's primary purpose is to be a direct expression of the BASF masterbrand.", 'activation_text': "The brand uses the non-negotiable BASF logo and corporate design.", 'examples': "Chemicals Division, Internal Initiatives"},
    'endorsed': {'recommendation': "BASF-Endorsed", 'rationale': "This entity has a proven need for a distinct identity to win. It has earned the right to a distinct brand, supported by an explicit link to the masterbrand.", 'activation_text': "The brand has its own identity but remains linked to BASF via a verbal or visual endorsement.", 'examples': "Chemetall, ECMS, Glasurit"},
    'independent': {'recommendation': "BASF-Independent", 'rationale': "This entity must be separate for legal, structural, or risk-insulation purposes.", 'activation_text': "The entity has full autonomy with no visible or verbal association with BASF.", 'examples': "Wintershall Dea, ExtractMax"},
    'flag_review': {'recommendation': "Flag for Strategic Review", 'rationale': "The evaluation has revealed a potential business misalignment.", 'activation_text': "This is not a branding recommendation but a business flag. It triggers a formal business review to determine the entity's future within the portfolio.", 'examples': "PolyWeld 800, No-Resource Product"},
    'follow_partner_guidelines': {'recommendation': "Follow Partner Guidelines", 'rationale': "As a third-party partner, branding is governed by specific legal and brand guidelines.", 'activation_text': "Consult the official 'Distributor Branding Guidelines' and engage with the Brand Consultancy team.", 'examples': "Third-Party Distributors"},
    'retire_rebrand': {'recommendation': "Independent (Retire & Rebrand)", 'rationale': "The acquired brand's negative equity is a liability.", 'activation_text': "The acquired brand identity will be retired. A formal plan must be created to migrate customers to a new or existing BASF brand.", 'examples': "OldChem Inc."},
    'follow_subsidiary_guidelines': {'recommendation': "Follow Subsidiary Guidelines / Treat as Independent", 'rationale': "This product is managed by an independent subsidiary. Its branding must follow the rules of its parent entity.", 'activation_text': "The branding for this product is not governed by the main BASF brand architecture. Please follow the established brand guidelines of the subsidiary.", 'examples': "A product created by Wintershall Dea"}
}

# --- UI HELPER FUNCTIONS ---
def display_interactive_image(image_path: str):
    # (Code from previous version - unchanged)
    ...

def show_examples(content_key):
    # (Code from previous version - unchanged)
    ...

# --- Main App ---
def run_app():
    if 'stage' not in st.session_state: st.session_state.stage = 0
    if 'entity_name' not in st.session_state: st.session_state.entity_name = ""
    if 'demo_key' not in st.session_state: st.session_state.demo_key = None

    def start_evaluation(name, demo_key=None):
        reset_app(full_reset=False)
        st.session_state.entity_name = name
        st.session_state.demo_key = demo_key
        set_stage(0.5)

    def set_stage(stage_num):
        st.session_state.stage = stage_num
        st.rerun()

    def reset_app(full_reset=True):
        password_correct = st.session_state.get("password_correct", False)
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        if full_reset:
            st.session_state.password_correct = password_correct
            st.rerun()
        
    def display_result(result_key):
        result = RESULT_DATA.get(result_key, {})
        st.header("Result")
        st.write(f"**Entity Evaluated:** *{st.session_state.entity_name}*")
        st.success(f"**Recommendation: {result.get('recommendation', 'N/A')}**")
        st.markdown(f"**Rationale:** {result.get('rationale', '')}")
        st.markdown("---")
        st.markdown(result.get('activation_text', ''))
        if result.get('examples'): st.markdown(f"**Similar Examples:** *{result.get('examples')}*")
        st.markdown("---")
        if st.button("Evaluate Another Entity"): reset_app()

    # --- UI FLOW ---
    if st.session_state.stage == 0:
        st.title("🧭 BASF Brand Compass")
        st.markdown("An interactive tool to provide clear, strategic direction for the BASF brand architecture.")
        st.subheader("Evaluate a New Entity")
        entity_name_input = st.text_input("Enter the name of the entity:", key="entity_name_input", label_visibility="collapsed")
        if st.button("Start Evaluation"):
            if entity_name_input: start_evaluation(entity_name_input)
            else: st.warning("Please enter an entity name.")

        st.markdown("---")
        st.subheader("Or, start with a guided demo:")
        
        st.markdown("**Standard Demos**")
        standard_demos = ["Chemicals", "Chemetall", "ECMS", "Coatings", "NewCo", "BASF Sonatrach PropanChem", "NewBiz", "Care 360°", "Insight 360", "Anniversaries", "Glasurit"]
        cols = st.columns(4)
        for i, brand_name in enumerate(standard_demos):
            with cols[i % 4]:
                demo_key = brand_name.lower().replace(' ', '').replace('°','')
                if st.button(brand_name, key=demo_key, use_container_width=True): start_evaluation(brand_name, demo_key=demo_key)

        st.markdown("---")
        st.subheader("Stress-Test Scenarios")
        st.markdown("""
        *   **PolyWeld 800:** A legacy product that is no longer core to strategy.
        *   **ExtractMax:** An entity operating in a controversial industry.
        *   **OldChem Inc.:** An acquired company with a negative reputation.
        *   **No-Resource Product:** A product team without the budget to support a distinct brand.
        """)
        stress_demos = {"PolyWeld 800": "polyweld800", "ExtractMax": "extractmax", "OldChem Inc.": "oldcheminc", "No-Resource Product": "noresourceproduct"}
        cols = st.columns(4)
        for name, key in stress_demos.items():
             if st.button(name, key=key, use_container_width=True): start_evaluation(name, demo_key=key)
        
        with st.expander("View the Brand Compass Flowchart"):
            display_interactive_image("flowchart.png")

    # --- STRATEGIC ROUTER & PATHWAYS ---
    else:
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        demo_data = DEMO_DATA.get(st.session_state.demo_key, {})
        stage_guidance = demo_data.get(f"stage{st.session_state.stage}", {})

        # STAGE 0.5: PURPOSE
        if st.session_state.stage == 0.5:
            st.subheader("Strategic Router: Purpose")
            choice = st.radio("What is the purpose of the entity?", ["Commercial", "Non-commercial"], index=demo_data.get('purpose', 0))
            if st.button("Next"):
                if choice == "Non-commercial": set_stage(0.6)
                else: set_stage(0.75)

        # STAGE 0.6: NON-COMMERCIAL
        elif st.session_state.stage == 0.6:
            st.subheader("Non-Commercial Audience")
            st.radio("What is the primary audience?", ["Internal", "External"], index=demo_data.get('audience', 0))
            if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
            display_result('basf_led')

        # STAGE 0.75: NATURE OF ENTITY
        elif st.session_state.stage == 0.75:
            st.subheader("Strategic Router: Nature of Entity")
            choice = st.radio("What is the nature of the entity?", ["Corporate Entity", "Product, Service, or Solution"], index=demo_data.get('nature', 0))
            if st.button("Next"):
                if choice.startswith("Corporate"):
                    st.session_state.path_type = 'corporate'
                    set_stage(1)
                else:
                    st.session_state.path_type = 'product'
                    set_stage(201)

        # --- CORPORATE PATH ---
        elif st.session_state.get('path_type') == 'corporate':
            st.markdown("*(Corporate Path)*")
            if st.session_state.stage == 1:
                st.subheader("Circuit Breaker 1: Ownership")
                options = ["Partner / Distributor", "Wholly Owned", "Joint Venture"]
                choice = st.radio("What is the ownership structure?", options, index=demo_data.get('ownership', 1))
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                if st.button("Next"):
                    if choice == options[0]: display_result('follow_partner_guidelines')
                    elif choice == options[1]: set_stage(1.1)
                    elif choice == options[2]: set_stage(1.2)

            elif st.session_state.stage == 1.1: # Wholly Owned
                choice = st.radio("Is it an acquisition?", ["Yes", "No"], index=demo_data.get('acquisition', 1))
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                if st.button("Next"):
                    if choice == "Yes": set_stage(1.11)
                    else: set_stage(4)

            elif st.session_state.stage == 1.11: # Acquisition
                choice = st.radio("Does the acquired brand have significant negative equity?", ["Yes", "No"], index=demo_data.get('negative_equity', 1))
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                if st.button("Next"):
                    if choice == "Yes": display_result('retire_rebrand')
                    else: set_stage(5)

            elif st.session_state.stage == 1.2: # JV
                choice = st.radio("What is BASF's equity share?", ["Majority (+50%)", "Minority (-50%)"], index=demo_data.get('jv_equity', 0))
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                if st.button("Next"):
                    if choice.startswith("Minority"): display_result('independent')
                    else: set_stage(4)

            elif st.session_state.stage == 4: # Resources
                st.subheader("Circuit Breaker: Resources")
                choice = st.radio("Will it have dedicated resources?", ["No", "Yes"], index=1)
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                if st.button("Next"):
                    if choice == "No": display_result('flag_review')
                    else: set_stage(3)

            elif st.session_state.stage == 3: # Legal
                st.subheader("Circuit Breaker: Legal Directives")
                choice = st.radio("Are there pre-existing legal/contractual requirements?", ["Yes", "No"], index=demo_data.get('legal', 1))
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                show_examples("Legal Directives")
                if st.button("Next"):
                    if choice == "Yes": display_result('flag_review')
                    else: set_stage(2)
            
            elif st.session_state.stage == 2: # Risk
                st.subheader("Circuit Breaker: Risk Profile")
                choice = st.radio("Does it have significant negative reputation potential?", ["Yes", "No"], index=demo_data.get('risk', 1))
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                show_examples("Risk Profile")
                if st.button("Next"):
                    if choice == "Yes": display_result('independent')
                    else: set_stage(5)

            elif st.session_state.stage == 5:
                st.subheader("Scorecard for Corporate Entities")
                st.warning("Scorecard functionality is under construction.")
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                if st.button("Calculate Recommendation (DEMO)"): display_result('endorsed')

        # --- PRODUCT PATH ---
        elif st.session_state.get('path_type') == 'product':
            st.markdown("*(Product Path)*")
            if st.session_state.stage == 201:
                st.subheader("Circuit Breaker 1: Governance")
                choice = st.radio("Is it managed by an Independent/non-BASF branded business?", ["Yes", "No"], index=demo_data.get('governance', 1))
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                if st.button("Next"):
                    if choice == "Yes": display_result('follow_subsidiary_guidelines')
                    else: set_stage(202)
            
            elif st.session_state.stage == 203:
                st.subheader("Circuit Breaker 3: Dependencies")
                choice = st.radio("Is it part of a larger offer?", ["Yes", "No"], index=demo_data.get('dependencies', 1))
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                if st.button("Next"):
                    if choice == "Yes": display_result('product_led')
                    else: set_stage(204)

            elif st.session_state.stage == 204:
                st.subheader("Circuit Breaker 4: Resources")
                choice = st.radio("Will it have dedicated resources?", ["No", "Yes"], index=demo_data.get('resources_prod', 1))
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                if st.button("Next"):
                    if choice == "No": display_result('flag_review')
                    else: set_stage(205)

            elif st.session_state.stage == 205:
                st.subheader("Scorecard for Products")
                st.warning("Scorecard functionality is under construction.")
                if stage_guidance.get('rationale'): st.info(f"**Demo Guidance:** {stage_guidance['rationale']}")
                if st.button("Calculate Recommendation (DEMO)"): display_result('product_endorsed')
            
            else: # Simplified Product Steps 202
                set_stage(203)

if check_password():
    run_app()
