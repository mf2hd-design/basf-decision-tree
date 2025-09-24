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

# --- Data Libraries (Reflecting V3 Logic) ---
# NOTE: This section is now much smaller as the logic is more complex than simple demos can capture.
# Demos now pre-select the path and first steps where applicable.
DEMO_DATA = {
    "chemetall": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 0, 'negative_equity': 1},
    "ecms": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 1},
    "coatings": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 1},
    "chemicals": {'purpose': 0, 'nature': 0, 'ownership': 1, 'acquisition': 1},
    "glasurit": {'purpose': 0, 'nature': 1},
    "internal_initiative": {'purpose': 1, 'audience': 0},
    "noncommercial_campaign": {'purpose': 1, 'audience': 1}
}


RESULT_DATA = {
    # Final Outcomes
    'basf_led': {'recommendation': "BASF-Led", 'rationale': "This entity's primary purpose is to be a direct expression of the BASF masterbrand. Its value is maximized by being an integral part of BASF.", 'activation_text': "The brand uses the non-negotiable BASF logo and corporate design. Flexibility is in communication and application style, but not in the core brand identity.", 'examples': "Chemicals Division, Internal Initiatives"},
    'endorsed': {'recommendation': "BASF-Endorsed", 'rationale': "This entity is strategically important but has a proven, data-backed need for a distinct identity to win in its market. It has earned the right to a distinct brand, supported by an explicit link to the masterbrand.", 'activation_text': "The brand has its own identity but remains linked to BASF via a verbal or visual endorsement. The scorecard results will recommend a default starting point on the endorsement spectrum (e.g., Co-branded, Prominent, or Distant) which can be adapted market-by-market with proper justification.", 'examples': "Chemetall, ECMS, Glasurit"},
    'independent': {'recommendation': "BASF-Independent", 'rationale': "This entity must be separate for legal, structural, or risk-insulation purposes. It operates with full autonomy to protect the masterbrand and/or comply with legal agreements.", 'activation_text': "The entity has full autonomy with no visible or verbal association with BASF. It must still adhere to BASF's non-negotiable core principles (Values Alignment, Legal Transparency of Ownership).", 'examples': "Wintershall Dea (Minority JV), ExtractMax (High Risk)"},
    'flag_review': {'recommendation': "Flag for Strategic Review", 'rationale': "The evaluation has revealed a potential misalignment between this entity's strategic importance and its required resources or market needs. This is a business issue, not a branding problem.", 'activation_text': "This is not a branding recommendation but a business flag. It triggers a formal business review to determine the entity's future within the portfolio.", 'examples': "An entity with low strategic contribution but high distinction needs."},
    # Circuit Breaker Outcomes
    'follow_partner_guidelines': {'recommendation': "Follow Partner Guidelines", 'rationale': "As a third-party partner with no BASF equity stake, branding is governed by specific legal and brand guidelines.", 'activation_text': "The primary action is to consult the official 'Distributor Branding Guidelines' and engage with the Brand Consultancy team to ensure full compliance before using any BASF branding.", 'examples': "Third-Party Distributors"},
    'retire_rebrand': {'recommendation': "Independent (Retire & Rebrand)", 'rationale': "The acquired brand's negative equity is a liability. The recommendation is to make it independent by retiring the name and transitioning customers to a BASF brand.", 'activation_text': "The acquired brand identity will be retired. A formal plan must be created to migrate customers and assets to a new or existing BASF brand, making the business independent of the problematic legacy name.", 'examples': "OldChem Inc."},
    'follow_subsidiary_guidelines': {'recommendation': "Follow Subsidiary Guidelines / Treat as Independent", 'rationale': "This product is deployed and managed by an independent or non-BASF branded subsidiary (e.g., a minority-owned JV). Its branding must follow the rules of its parent entity.", 'activation_text': "The branding for this product is not governed by the main BASF brand architecture. It should be treated as 'Independent' from a BASF portfolio perspective. Please follow the established brand guidelines of the subsidiary that manages the product.", 'examples': "A product created by Wintershall Dea"}
}

# --- UI HELPER FUNCTIONS ---
def display_interactive_image(image_path: str):
    # (Code from previous version - unchanged)
    ...

def show_examples(content_key):
    st.markdown("---")
    with st.expander(f"**Click here to see illustrative examples for {content_key}**"):
        if content_key == "Risk Profile":
            st.markdown("""
            - **Operating in Controversial Industries:** Our stress-test case, "ExtractMax," a product used in a highly controversial industry (e.g., oil sands). The association could lead to negative press against the entire BASF group, forcing an "Independent" status to create a reputational firewall.
            - **High-Risk / Unproven Technologies:** A new venture exploring a cutting-edge but publicly controversial technology (e.g., certain types of genetic modification). Until the technology is proven safe and socially accepted, a direct link to BASF is too risky.
            - **Association with Sanctioned or High-Risk Geographies:** A business unit that operates almost exclusively in a country with a high risk of political instability or international sanctions.
            """)
        elif content_key == "Legal Directives":
            st.markdown("""
            - **Joint Venture (JV) Agreements:** The "BASF SONATRACH PropanChem" joint venture. The legal agreement explicitly states that both parent companies' names must be used. This is a non-negotiable legal directive.
            - **Acquisition / Divestiture Terms:** An agreement might state that BASF can only use an acquired brand's name for a transition period of 24 months, after which it must be retired.
            - **Brand Licensing Agreements:** A partner is licensed to use a BASF ingredient. The contract will have strict rules about how the BASF brand can be mentioned (e.g., "contains ingredient X from BASF"), but legally prevents the partner from calling their product a "BASF product."
            """)

def render_scorecard_question(q_id, q_text, evidence_text, rationale_text, weight, demo_value=False):
    with st.expander(q_text):
        st.info(f"**Evidence Guide:** {evidence_text}")
        st.markdown(f"**Rationale:** {rationale_text}")
    is_checked = st.checkbox("Select if applicable", key=q_id, value=demo_value)
    if is_checked:
        return weight
    return 0

# --- Main App ---
def run_app():
    # Initialize session state
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
        if result.get('examples'):
            st.markdown(f"**Similar Examples:** *{result.get('examples')}*")
        st.markdown("---")
        if st.button("Evaluate Another Entity"):
            reset_app()

    # --- UI FLOW ---
    if st.session_state.stage == 0:
        st.title("🧭 BASF Brand Compass")
        st.markdown("An interactive tool to provide clear, strategic direction for the BASF brand architecture.")
        st.subheader("Evaluate a New Entity")
        entity_name_input = st.text_input("Enter the name of the entity:", key="entity_name_input", label_visibility="collapsed")
        if st.button("Start Evaluation"):
            if entity_name_input:
                start_evaluation(entity_name_input)
            else:
                st.warning("Please enter an entity name.")

        st.markdown("---")
        st.subheader("Or, start with a guided demo:")
        demos = {"Chemetall": "chemetall", "ECMS": "ecms", "Coatings": "coatings", "Chemicals": "chemicals", "Glasurit": "glasurit", "Internal Initiative": "internal_initiative"}
        cols = st.columns(4)
        for i, (name, key) in enumerate(demos.items()):
            with cols[i % 4]:
                if st.button(name, key=key, use_container_width=True):
                    start_evaluation(name, demo_key=key)
        
    # --- STRATEGIC ROUTER ---
    elif st.session_state.stage == 0.5:
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        st.subheader("Strategic Router: Purpose")
        demo_val = DEMO_DATA.get(st.session_state.demo_key, {}).get('purpose', 0)
        choice = st.radio("What is the purpose of the entity being evaluated?", ["Commercial", "Non-commercial"], index=demo_val)
        if st.button("Next"):
            if choice == "Non-commercial":
                set_stage(0.6)
            else:
                set_stage(0.75)

    elif st.session_state.stage == 0.6:
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        st.subheader("Non-Commercial Audience")
        demo_val = DEMO_DATA.get(st.session_state.demo_key, {}).get('audience', 0)
        st.radio("What is the primary audience?", ["Internal", "External (e.g., temporary campaign)"], index=demo_val)
        display_result('basf_led')

    elif st.session_state.stage == 0.75:
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        st.subheader("Strategic Router: Nature of Entity")
        demo_val = DEMO_DATA.get(st.session_state.demo_key, {}).get('nature', 0)
        choice = st.radio("What is the nature of the entity?", ["Corporate Entity (Company, Division, Business Unit)", "Product, Service, or Solution"], index=demo_val)
        if st.button("Next"):
            if choice.startswith("Corporate"):
                st.session_state.path_type = 'corporate'
                set_stage(1)
            else:
                st.session_state.path_type = 'product'
                set_stage(201)

    # --- CORPORATE PATH ---
    elif st.session_state.path_type == 'corporate':
        st.header(f"Evaluating: *{st.session_state.entity_name}* (Corporate Path)")
        demo_data = DEMO_DATA.get(st.session_state.demo_key, {})

        if st.session_state.stage == 1:
            st.subheader("Circuit Breaker 1: Ownership")
            options = ["Partner / Distributor", "Wholly Owned", "Joint Venture"]
            choice = st.radio("What is the ownership structure?", options, index=demo_data.get('ownership', 1))
            if st.button("Next"):
                if choice == options[0]: display_result('follow_partner_guidelines')
                elif choice == options[1]: set_stage(1.1)
                elif choice == options[2]: set_stage(1.2)

        elif st.session_state.stage == 1.1: # Wholly Owned Branch
            choice = st.radio("Is it an acquisition?", ["Yes", "No"], index=demo_data.get('acquisition', 1))
            if st.button("Next"):
                if choice == "Yes": set_stage(1.11)
                else: set_stage(4) # Skip to Resources

        elif st.session_state.stage == 1.11: # Acquisition Branch
            choice = st.radio("Does the acquired brand have significant negative equity?", ["Yes", "No"], index=demo_data.get('negative_equity', 1))
            if st.button("Next"):
                if choice == "Yes": display_result('retire_rebrand')
                else: set_stage(5) # Go to Scorecard

        elif st.session_state.stage == 1.2: # JV Branch
            choice = st.radio("What is BASF's equity share?", ["Majority (+50%)", "Minority (-50%)"])
            if st.button("Next"):
                if choice.startswith("Minority"): display_result('independent')
                else: set_stage(4) # Go to Resources

        elif st.session_state.stage == 4:
            st.subheader("Circuit Breaker 2: Resources")
            choice = st.radio("Will it have dedicated and approved resources to support multi-year identity and marketing efforts?", ["No", "Yes"], index=1)
            if st.button("Next"):
                if choice == "No": display_result('flag_review')
                else: set_stage(3)

        elif st.session_state.stage == 3:
            st.subheader("Circuit Breaker 3: Legal Directives")
            choice = st.radio("Are there any pre-existing legal or contractual requirements that dictate the brand identity?", ["Yes", "No"], index=1)
            show_examples("Legal Directives")
            if st.button("Next"):
                if choice == "Yes": display_result('flag_review') # Or a more specific 'follow legal'
                else: set_stage(2)
        
        elif st.session_state.stage == 2:
            st.subheader("Circuit Breaker 4: Risk Profile")
            choice = st.radio("Does it have the potential to create significant negative reputation impact for BASF?", ["Yes", "No"], index=1)
            show_examples("Risk Profile")
            if st.button("Next"):
                if choice == "Yes": display_result('independent')
                else: set_stage(5)

        elif st.session_state.stage == 5:
            # Corporate Scorecard implementation...
            st.subheader("Scorecard for Corporate Entities")
            # (Content of scorecard goes here, using render_scorecard_question helper)
            st.warning("Corporate Scorecard Section is under construction.")
            if st.button("Calculate Recommendation (DEMO)"):
                display_result('endorsed')


    # --- PRODUCT PATH ---
    elif st.session_state.path_type == 'product':
        st.header(f"Evaluating: *{st.session_state.entity_name}* (Product Path)")
        
        if st.session_state.stage == 201:
            st.subheader("Circuit Breaker 1: Governance")
            choice = st.radio("Will it be deployed and managed by an Independent business that currently does not use the BASF brand?", ["Yes", "No"], index=1)
            if st.button("Next"):
                if choice == "Yes": display_result('follow_subsidiary_guidelines')
                else: set_stage(202)
        
        elif st.session_state.stage == 202:
            st.subheader("Circuit Breaker 2: Ownership")
            # Simplified for now, can be expanded
            st.radio("What is the ownership structure?", ["Wholly Owned"])
            if st.button("Next"):
                set_stage(203)
        
        elif st.session_state.stage == 203:
            st.subheader("Circuit Breaker 3: Dependencies")
            choice = st.radio("Will it go to market as part of a larger offer or value proposition?", ["Yes", "No"], index=1)
            if st.button("Next"):
                if choice == "Yes": display_result('product_led') # Treat as feature
                else: set_stage(204)

        # Simplified remaining product circuit breakers for brevity
        elif st.session_state.stage == 204:
            st.subheader("Final Checks")
            st.write("Assuming product passes Risk, Legal, and Resource checks...")
            if st.button("Proceed to Scorecard"):
                set_stage(205)

        elif st.session_state.stage == 205:
            # Product Scorecard implementation...
            st.subheader("Scorecard for Products, Services, or Solutions")
            st.warning("Product Scorecard Section is under construction.")
            if st.button("Calculate Recommendation (DEMO)"):
                display_result('product_endorsed')

if check_password():
    run_app()
