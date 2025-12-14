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
    """Returns `True` if the user is logged in."""
    def password_entered():
        if st.session_state.get("password") == "2025FFxBASFxFF":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.title("🧭 The BASF Brand Compass")
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password" in st.session_state and not st.session_state.get("password_correct", False):
        st.error("😕 Password incorrect")
    return False

# --- Data Libraries (Full Library Restored) ---
DEMO_DATA = {
    # --- Corporate Path Demos ---
    "chemicals": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a1': True, 'a2': True, 'a4': True, 'a5': True}, 'score_B_checks': {}, 'rationale': "As the core engine of BASF, its contribution is maximum. Its entire value comes from being BASF."}},
    "chemovator": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a1': True, 'a2': True, 'a3': True}, 'score_B_checks': {'b2': True, 'b3': True}, 'rationale': "Innovation pillar requiring distinct identity for agility and talent attraction."}},
    "newbiz": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a3': True}, 'score_B_checks': {'b2': True, 'b3': True, 'b4': True}, 'rationale': "Exploratory venture with high need for distinction in new fields."}},
    "coatings": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a1': True, 'a3': True, 'a5': True}, 'score_B_checks': {'b3': True, 'b4': True}, 'rationale': "Growth pillar competing with pure-players."}},
    "ecms": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a2': True, 'a3': True, 'a4': True}, 'score_B_checks': {'b3': True, 'b4': True}, 'rationale': "Sustainability-focused growth pillar needing distinct identity."}},
    "care360": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a2': True, 'a4': True}, 'score_B_checks': {}, 'rationale': "Solutions platform embodying BASF."}},
    
    # --- Corporate Path Off-Ramps ---
    "newco": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 0}, 'stage1.2': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {}, 'score_B_checks': {}, 'rationale': "Acquisition with positive equity."}},
    "basfsonatrachpropanchem": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 2}, 'stage1.3': {'index': 0}, 'stage2': {'index': 1}, 'stage3': {'index': 0, 'rationale': "Joint Venture governed by legal agreement."}},
    "insight360": {'path': 'corporate', 'stage0.5': {'index': 1, 'rationale': "Internal tool considered Non-commercial."}},
    "anniversaries": {'path': 'corporate', 'stage0.5': {'index': 1, 'rationale': "Temporary campaign considered Non-commercial."}},

    # --- Stress-Test Demos ---
    "polyweld800business": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {}, 'score_B_checks': {}, 'rationale': "Legacy business with low strategic contribution."}},
    "extractmax": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 0, 'rationale': "Controversial industry triggering risk off-ramp."}},
    "oldcheminc": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 0}, 'stage1.2': {'index': 0, 'rationale': "Acquisition with negative reputation."}},

    # --- Product Path Demos ---
    "glasurit": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 1}, 'stage202.1': {'index': 1}, 'stage203': {'index': 1}, 'stage204': {'index': 1}, 'stage205': {'index': 1}, 'stage206': {'score_A_checks': {'pa1': True, 'pa2': True, 'pa3': True, 'pa4': True}, 'score_B_checks': {'pb1': True, 'pb2': True}, 'data_mandate': "Competes against consumer-facing refinish brands.", 'rationale': "Cornerstone of Coatings division."}},
    "ultramid": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 1}, 'stage202.1': {'index': 1}, 'stage203': {'index': 1}, 'stage204': {'index': 1}, 'stage205': {'index': 1}, 'stage206': {'score_A_checks': {'pa1': True, 'pa2': True, 'pa4': True, 'pa5': True}, 'score_B_checks': {}, 'data_mandate': "N/A - No distinction needed.", 'rationale': "Workhorse ingredient brand."}},
    
    # --- Product Path Stress-Tests ---
    "noresourceproduct": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 1}, 'stage202.1': {'index': 1}, 'stage203': {'index': 1}, 'stage204': {'index': 1}, 'stage205': {'index': 0, 'rationale': "Lacks dedicated budget."}},
    "jvproduct": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 2, 'rationale': "Product belongs to a JV."}}
}

RESULT_DATA = {
    # Corporate Path Outcomes (Updated Terminology)
    'basf_led': {'recommendation': "BASF Branded", 'rationale': "This entity's primary purpose is to be a direct expression of the BASF masterbrand. Its value is maximized by being an integral part of BASF.", 'activation_text': "This means we don't create a separate brand. The entity is branded simply as 'BASF [Entity Name]'. It lives on the main BASF website and is sold by the BASF sales team, reinforcing the power and innovation of the masterbrand.", 'examples': "Chemicals Division, Internal Tools"},
    'endorsed_level1': {'recommendation': "BASF-Endorsed (Level 1: Co-Branded Lockup)", 'rationale': "This entity is a strategically critical pillar but requires its own distinct identity to win. The recommendation is a tight, explicit endorsement.", 'activation_text': "This triggers the **Co-Branded Lockup** playbook. The entity will have its own distinct brand identity but must use a mandatory visual co-branding system with the BASF logo.", 'examples': "Chemovator GmbH"},
    'endorsed_level2': {'recommendation': "BASF-Endorsed (Level 2: Prominent Verbal Endorsement)", 'rationale': "This entity is an important, established brand that needs its own space but gains significant credibility from an explicit BASF link.", 'activation_text': "This triggers the **Prominent Verbal Endorsement** playbook. The brand operates with its own identity, supported by the classic 'powered by BASF' or 'A BASF Company' tagline.", 'examples': "Coatings Division Brands"},
    'endorsed_level3': {'recommendation': "BASF-Endorsed (Level 3: Distant Verbal Endorsement)", 'rationale': "This entity is an exploratory venture that needs maximum independence. A subtle, distant link provides a 'halo' of quality while insulating the masterbrand from risk.", 'activation_text': "This triggers the **Distant Endorsement** playbook. The brand operates with full independence. The connection to BASF is strategic and not part of the primary brand identity.", 'examples': "NewBiz (Hypothetical), Metivo"},
    'flag_review': {'recommendation': "Flag for Strategic Review", 'rationale': "This entity's profile indicates a misalignment. This could be due to low strategic importance, a lack of resources, or other factors. This is a business issue, not just a branding problem.", 'activation_text': "This is not a branding recommendation but a business flag. The entity's situation warrants a formal business review to determine its future within the portfolio.", 'examples': "PolyWeld 800 Business"},
    
    # Product Path Outcomes (Updated Terminology)
    'product_led': {'recommendation': "BASF Branded (Product Level)", 'rationale': "This product's value is maximized by leveraging the full trust and equity of the BASF masterbrand. There is no data-backed business case for a distinct identity.", 'activation_text': "The recommendation is to use the standard **'BASF Productname®'** lockup. This approach ensures market clarity, reinforces BASF's quality promise, and provides the strongest return on investment.", 'examples': "Ultramid®"},
    'product_endorsed': {'recommendation': "BASF-Endorsed (Product Level)", 'rationale': "This product is a cornerstone of a divisional strategy and has a proven, data-backed need for a distinct identity to win.", 'activation_text': "This product has earned the right to a distinct brand identity. It must be supported by a mandatory, explicit endorsement (e.g., 'powered by BASF').", 'examples': "Glasurit®"},
    'insufficient_resources': {'recommendation': "Flag for Review (Insufficient Resources)", 'rationale': "Building and sustaining a distinct brand requires significant, long-term investment. Without dedicated resources, a new brand identity cannot succeed.", 'activation_text': "The entity does not have the required resources to support a distinct brand. This triggers a **Flag for Review**.", 'examples': "Any product without a dedicated brand budget"},
    'evaluate_parent_entity': {'recommendation': "Evaluate Parent Entity First", 'rationale': "A product's branding cannot be decided until its parent company's relationship to BASF is defined.", 'activation_text': "This product belongs to an entity that is not wholly-owned by BASF (e.g., a Joint Venture). Please use the **Corporate Path** to evaluate the parent corporate entity first.", 'examples': "Products from a Joint Venture"},
    
    # General Outcomes
    'not_governed_by_basf': {'recommendation': "Not Governed by BASF Brand", 'rationale': "The entity is deployed and managed by an independent business that does not currently use the BASF brand.", 'activation_text': "This entity falls outside the governance of the BASF brand architecture. The recommendation is to treat it as 'Independent'.", 'examples': "Wintershall Dea subsidiary"},
    'legal_directive': {'recommendation': "Follow Legal Directive", 'rationale': "A binding legal or contractual agreement decides the branding for this entity.", 'activation_text': "The primary action is to consult the specific legal documents (e.g., the Joint Venture agreement) and implement the branding exactly as specified.", 'examples': "BASF SONATRACH PropanChem"},
    'independent_risk': {'recommendation': "Independent (Risk Insulation)", 'rationale': "The entity has the potential to create significant negative reputation impact or channel conflict.", 'activation_text': "This means the entity must operate as a fully independent brand with no visible connection to BASF. This is a strategic decision to create a 'reputational firewall'.", 'examples': "ExtractMax"},
    'follow_partner_guidelines': {'recommendation': "Follow Partner/Distributor Guidelines", 'rationale': "As a third-party partner/distributor with no BASF equity stake, branding is governed by specific legal and brand guidelines.", 'activation_text': "The primary action is to consult the official 'Distributor Branding Guidelines'.", 'examples': "Third-Party Distributors"},
    'independent_minority': {'recommendation': "Independent (Minority-owned JV)", 'rationale': "As a minority stakeholder (<50% equity), BASF cannot enforce its brand identity.", 'activation_text': "This entity requires its own independent brand identity. BASF's involvement should be communicated strategically as an endorsement or partnership.", 'examples': "Minority-stake Joint Ventures"},
    'retire_rebrand': {'recommendation': "Independent (Retire & Rebrand)", 'rationale': "The acquired brand has negative equity/reputation, making its association a liability.", 'activation_text': "This means the acquired brand identity will be retired. A formal plan must be created to migrate customers and assets to a new or existing BASF brand.", 'examples': "OldChem Inc."}
}

WEIGHTS = {
    'corporate_A': {'a1': 3, 'a2': 3, 'a3': 2, 'a4': 2, 'a5': 1},
    'corporate_B': {'b1': 3, 'b2': 3, 'b3': 2, 'b4': 2, 'b5': 1},
    'product_A': {'pa1': 3, 'pa2': 3, 'pa3': 2, 'pa4': 2, 'pa5': 1},
    'product_B': {'pb1': 3, 'pb2': 3, 'pb3': 2, 'pb4': 2, 'pb5': 1}
}
HIGH_THRESHOLD = 6


# --- Main App Function ---
def run_app():
    # Initialize session state
    if 'stage' not in st.session_state: st.session_state.stage = 0
    if 'entity_name' not in st.session_state: st.session_state.entity_name = ""
    if 'scores' not in st.session_state: st.session_state.scores = {'A': 0, 'B': 0}
    if 'demo_key' not in st.session_state: st.session_state.demo_key = None
    if 'path_type' not in st.session_state: st.session_state.path_type = None

    def start_evaluation(entity_name, is_demo=False, demo_key=None):
        st.session_state.entity_name = entity_name
        if is_demo and demo_key:
            st.session_state.demo_key = demo_key
            st.session_state.path_type = DEMO_DATA[demo_key].get('path', 'corporate')
        set_stage(0.5)

    def set_stage(stage_num):
        st.session_state.stage = stage_num
        st.rerun()

    def reset_app_callback():
        keys_to_delete = [key for key in st.session_state.keys() if key != 'password_correct']
        for key in keys_to_delete:
            del st.session_state[key]
        st.session_state.stage = 0
    
    def display_result(result_key):
        result = RESULT_DATA.get(result_key, {'recommendation': 'Error', 'rationale': 'Result key not found.', 'activation_text': '', 'examples': ''})
        st.header("Result")
        st.write(f"**Entity Evaluated:** *{st.session_state.entity_name}*")
        st.markdown("---")
        st.subheader("Activation Guide")
        st.caption("This final phase provides the actionable guide for execution.")
        st.success(f"**Recommendation: {result['recommendation']}**")
        st.markdown(f"**Rationale:** {result['rationale']}")
        st.markdown("---")
        st.markdown(result['activation_text'])
        if result.get('examples'):
            st.markdown(f"**Similar Examples:** *{result['examples']}*")
        st.markdown("---")
        st.button("Evaluate Another Entity", on_click=reset_app_callback)
    
    st.title("🧭 The BASF Brand Compass")
    if st.session_state.stage == 0:
        # --- HOME PAGE ---
        st.markdown("An interactive tool to provide clear, strategic direction for the BASF brand architecture.")
        st.subheader("Evaluate a New Entity")
        entity_name_input = st.text_input("Enter name:", key="entity_name_input", label_visibility="collapsed")
        if st.button("Start Manual Evaluation"):
            if entity_name_input: start_evaluation(entity_name_input)
            else: st.warning("Please enter an entity name to begin.")
        st.markdown("---")
        st.subheader("Or, start a guided demo for a known brand:")

        st.markdown("**Standard Demos (Corporate-Level)**")
        standard_demos = ["Chemicals", "Chemovator", "NewBiz", "BASF Sonatrach PropanChem", "NewCo", "Anniversaries", "Coatings", "ECMS", "Care 360°", "Insight 360"]
        cols = st.columns(4)
        for i, brand_name in enumerate(standard_demos):
            with cols[i % 4]:
                demo_key = brand_name.lower().replace(' ', '').replace('°','')
                if st.button(brand_name, key=demo_key, use_container_width=True): start_evaluation(brand_name, is_demo=True, demo_key=demo_key)

        st.markdown("**Product-Level Demos**")
        product_demos = ["Glasurit", "Ultramid"]
        cols = st.columns(4)
        for i, brand_name in enumerate(product_demos):
            with cols[i % 4]:
                demo_key = brand_name.lower()
                if st.button(brand_name, key=demo_key, use_container_width=True): start_evaluation(brand_name, is_demo=True, demo_key=demo_key)

        st.markdown("---")
        st.subheader("Stress-Test Scenarios")
        
        # --- STRESS TEST DEMOS ---
        stress_demos = {
            "PolyWeld 800 Business": {
                "key": "polyweld800business",
                "caption": "Tests a legacy business with low strategic contribution."
            },
            "ExtractMax": {
                "key": "extractmax",
                "caption": "Tests the reputational risk Fast Track for a controversial entity."
            },
            "OldChem Inc.": {
                "key": "oldcheminc",
                "caption": "Tests the acquisition path for a company with negative brand equity."
            },
            "No-Resource Product": {
                "key": "noresourceproduct",
                "caption": "Tests the product path for an entity that lacks a dedicated budget."
            },
            "JV Product": {
                "key": "jvproduct",
                "caption": "Tests the product path for an item belonging to a Joint Venture."
            }
        }
        cols = st.columns(len(stress_demos))
        for i, (name, data) in enumerate(stress_demos.items()):
            with cols[i]:
                if st.button(name, key=data["key"], use_container_width=True):
                    start_evaluation(name, is_demo=True, demo_key=data["key"])
                st.caption(data["caption"])

        # --- EXPANDER WITH PDF DOWNLOAD BUTTON ---
        with st.expander("View the Brand Compass Decision Tree PDF"):
            try:
                with open("document.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()

                st.download_button(
                    label="Download the Decision Tree PDF",
                    data=PDFbyte,
                    file_name="BASF_Decision_Tree.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.caption("Click to download the full PDF.")
            except FileNotFoundError:
                st.error("File not found: 'document.pdf'.")


    elif st.session_state.stage == 0.5:
        # --- STRATEGIC ROUTER (V3) ---
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        st.subheader("Strategic Router")
        st.markdown("""
        **What is the purpose of the entity being evaluated?**

        *   **Commercial:** Choose this if the entity is **market-facing and has its own Profit & Loss (P&L)**.
            *   *Examples: A business unit, a subsidiary company, a product line.*
        
        *   **Non-commercial:** Choose this for **any other activity, even if it supports commercial goals.**
            *   *Examples: Marketing campaigns, events, trade fairs, internal initiatives, R&D projects.*
        """)
        
        path_options = ["Commercial", "Non-commercial"]
        demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage0.5', {})
        rec_index = demo_data.get('index')
        
        path_choice = st.radio("Select the entity's purpose:", path_options, index=rec_index, key="purpose_router")
        
        if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")

        if st.button("Proceed"):
            if path_choice == path_options[1]: # Non-commercial
                display_result('basf_led')
            else: # Commercial
                set_stage(0.6)

    elif st.session_state.stage == 0.6:
        # --- ENTITY TYPE ROUTER ---
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        st.subheader("Strategic Router")
        st.write("**What is the nature of the entity?**")
        
        path_options = ["Corporate Entity (e.g., a company, JV, business unit)", "Product, Service, or Solution"]
        
        demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage0.6', {})
        rec_index = demo_data.get('index')
        
        path_choice = st.radio("Select the entity type:", path_options, index=rec_index, key="path_router", label_visibility="collapsed")
        
        if st.button("Proceed"):
            if path_choice == path_options[0]:
                st.session_state.path_type = 'corporate'
                set_stage(1) # Start of Corporate Path
            else:
                st.session_state.path_type = 'product'
                set_stage(201) # Start of Product Path
    
    else:
        # --- CORPORATE PATH ---
        if st.session_state.path_type == 'corporate':
            st.header(f"Evaluating: *{st.session_state.entity_name}* (Corporate Path)")
            
            if st.session_state.stage == 1:
                st.subheader("Fast Track 1: Ownership")
                st.write("**What is the ownership structure?**")
                options = ["Partner / Distributor", "Wholly Owned", "Joint Venture"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1', {})
                choice = st.radio("Select ownership structure:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == options[0]: display_result('follow_partner_guidelines')
                    elif choice == options[1]: set_stage(1.1)
                    else: set_stage(1.3)
            
            elif st.session_state.stage == 1.1:
                st.subheader("Fast Track 1: Ownership")
                st.write("**Is it an acquisition?**")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.1', {})
                choice = st.radio("Select if it is an acquisition:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": set_stage(1.2)
                    else: set_stage(2)
            
            elif st.session_state.stage == 1.2:
                st.subheader("Fast Track 1: Ownership")
                st.write("**Does the acquired brand have Negative Brand Equity?**")
                st.caption("E.g., known bad reputation, scandal, or safety failures.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.2', {})
                choice = st.radio("Select if it has negative equity:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('retire_rebrand')
                    else: set_stage(2)

            elif st.session_state.stage == 1.3:
                st.subheader("Fast Track 1: Ownership")
                st.write("**What is BASF's ownership share in the Joint Venture?**")
                options = ["Majority (50% or more)", "Minority (less than 50%)"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.3', {})
                choice = st.radio("Select ownership share:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == options[1]: display_result('independent_minority')
                    else: set_stage(2)

            elif st.session_state.stage == 2:
                st.subheader("Fast Track 2: Risk Profile")
                st.write("**Could it harm BASF's reputation?**")
                st.caption("Examples: Controversial industry, channel conflict with key customers, or high-risk technology.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage2', {})
                choice = st.radio("Select if there is a potential for negative impact:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('independent_risk')
                    else: set_stage(3)

            elif st.session_state.stage == 3:
                st.subheader("Fast Track 3: Legal Directives")
                st.write("**Does a legal contract already decide the brand?**")
                st.caption("E.g., Joint Venture agreement or licensing deal.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage3', {})
                choice = st.radio("Select if a contract decides the brand:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('legal_directive')
                    else: set_stage(4)

            elif st.session_state.stage == 4:
                st.subheader("Fast Track 4: Resources")
                st.write("**Does it have dedicated Brand Management resources?**")
                st.caption("This means budget/team for design, research, and long-term brand building, not just product marketing.")
                options = ["No", "Yes"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage4', {})
                choice = st.radio("Select if resources are dedicated:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "No": display_result('flag_review')
                    else: set_stage(5)

            elif st.session_state.stage == 5:
                st.subheader("Strategic Scorecard")
                st.caption("The entity has passed all Fast Tracks. Now, score its value to BASF and its need for a separate brand.")
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage5', {})
                rec_A = demo_data.get('score_A_checks', {})
                rec_B = demo_data.get('score_B_checks', {})
                
                questions_A = { 
                    'a1': 'Linked to a top priority of BASF\'s business strategy?', 
                    'a2': 'Helps achieve a major company goal or performance target (KPI)?', 
                    'a3': 'Wins in a new market, segment, or business model?', 
                    'a4': 'Strongly supports or demonstrates our desired brand character/positioning?', 
                    'a5': "Relies on deep operational integration with BASF's core capabilities?" 
                }
                questions_B = { 
                    'b1': 'Known negative view of the BASF brand for this specific audience?', 
                    'b2': 'Market has norms/expectations misaligned with BASF conventional practices?', 
                    'b3': 'Competes primarily against specialised "pure-players"?', 
                    'b4': 'Direct-to-consumer sales requiring specific consumer marketing language?', 
                    'b5': 'Distinct way of working forming a unique value proposition?' 
                }
                
                score_A, score_B = 0, 0
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Part A: Strategic Contribution**")
                    for key, q_text in questions_A.items():
                        if st.checkbox(q_text, value=rec_A.get(key, False), key=key): 
                            score_A += WEIGHTS['corporate_A'][key]
                        if key == 'a5':
                            st.caption("A 'No' is common for agile, standalone ventures. A 'Yes' is typical for businesses that use shared resources.")

                    st.session_state.scores['A'] = score_A
                    st.write(f"**Score A: {score_A} / 11**")
                with col2:
                    st.info("**Part B: Market Distinction**")
                    for key, q_text in questions_B.items():
                        if st.checkbox(q_text, value=rec_B.get(key, False), key=key): score_B += WEIGHTS['corporate_B'][key]
                    st.session_state.scores['B'] = score_B
                    st.write(f"**Score B: {score_B} / 11**")
                
                if st.button("Calculate Recommendation"): set_stage(6)

            elif st.session_state.stage == 6:
                score_a, score_b = st.session_state.scores['A'], st.session_state.scores['B']
                score_a_high = score_a >= HIGH_THRESHOLD
                score_b_high = score_b >= HIGH_THRESHOLD
                outcome_key = ''
                if score_a_high and not score_b_high: outcome_key = 'basf_led'
                elif score_a_high and score_b_high: outcome_key = 'endorsed_level1'
                elif not score_a_high and score_b_high: outcome_key = 'endorsed_level3'
                else: outcome_key = 'flag_review'
                if (4 <= score_a < HIGH_THRESHOLD) and (4 <= score_b < HIGH_THRESHOLD):
                    outcome_key = 'endorsed_level2'
                display_result(outcome_key)

        # --- PRODUCT PATH ---
        elif st.session_state.path_type == 'product':
            st.header(f"Evaluating: *{st.session_state.entity_name}* (Product Path)")

            if st.session_state.stage == 201:
                st.subheader("Fast Track 1: Governance")
                st.write("**Is it managed by an independent business outside the BASF brand?**")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage201', {})
                choice = st.radio("Select an answer:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('not_governed_by_basf')
                    else: set_stage(202)

            elif st.session_state.stage == 202:
                st.subheader("Fast Track 2: Ownership")
                options = ["Partner / Distributor", "Wholly Owned", "Joint Venture"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202', {})
                choice = st.radio("Select ownership structure:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == options[0]: display_result('follow_partner_guidelines')
                    elif choice == options[1]: set_stage(202.1)
                    else: set_stage(202.2)

            elif st.session_state.stage == 202.1:
                st.subheader("Fast Track 2: Ownership")
                st.write("**Is it an acquisition?**")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202.1', {})
                choice = st.radio("Select if it is an acquisition:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": set_stage(202.3)
                    else: set_stage(203)

            elif st.session_state.stage == 202.2:
                st.subheader("Fast Track 2: Ownership")
                st.write("Products from a Joint Venture must follow the parent company's brand.")
                if st.button("Show Recommendation"):
                    display_result('evaluate_parent_entity')

            elif st.session_state.stage == 202.3:
                st.subheader("Fast Track 2: Ownership")
                st.write("**Does the acquired brand have Negative Brand Equity?**")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202.3', {})
                choice = st.radio("Select if it has negative equity:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('retire_rebrand')
                    else: set_stage(203)

            elif st.session_state.stage == 203:
                st.subheader("Fast Track 3: Risk Profile")
                st.write("**Could it harm BASF's reputation?**")
                st.caption("E.g., Controversial industry, channel conflict, or high-risk technology.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage203', {})
                choice = st.radio("Select if there is a potential for negative impact:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('independent_risk')
                    else: set_stage(204)

            elif st.session_state.stage == 204:
                st.subheader("Fast Track 4: Legal Directives")
                st.write("**Does a legal contract already decide the brand?**")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage204', {})
                choice = st.radio("Select if a contract decides the brand:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('legal_directive')
                    else: set_stage(205)

            elif st.session_state.stage == 205:
                st.subheader("Fast Track 5: Resources")
                st.write("**Does it have dedicated Brand Management resources?**")
                st.caption("Multi-year budget for design, research, and management.")
                options = ["No", "Yes"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage205', {})
                choice = st.radio("Select if resources are dedicated:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "No": display_result('insufficient_resources')
                    else: set_stage(206)

            elif st.session_state.stage == 206:
                st.subheader("Product Scorecard")
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage206', {})
                rec_A = demo_data.get('score_A_checks', {})
                rec_B = demo_data.get('score_B_checks', {})
                rec_data = demo_data.get('data_mandate', "")
                questions_A = { 
                    'pa1': 'Top priority for a major business division\'s strategy?', 
                    'pa2': 'Creates positive "halo effect" for the main BASF brand?', 
                    'pa3': 'Accesses new, important customer group or market?', 
                    'pa4': 'Proven high value creation (revenue/margin)?', 
                    'pa5': 'Represents breakthrough technology or innovation?' 
                }
                questions_B = { 
                    'pb1': 'Does data prove it needs its own brand to avoid confusing customers/cannibalisation?', 
                    'pb2': 'Does data prove it needs to appeal directly to consumers (B2C)?', 
                    'pb3': 'Does data prove it competes against specialised "pure-player" brands?', 
                    'pb4': 'Does it require a unique selling method (e.g., e-commerce)?', 
                    'pb5': 'Does data prove the BASF name is a negative factor for the target customer?' 
                }
                score_A, score_B = 0, 0
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Part A: Strategic Contribution**")
                    for key, q_text in questions_A.items():
                        if st.checkbox(q_text, value=rec_A.get(key, False), key=key): score_A += WEIGHTS['product_A'][key]
                    st.session_state.scores['A'] = score_A
                    st.write(f"**Score A: {score_A} / 11**")
                with col2:
                    st.info("**Part B: Market Distinction**")
                    st.caption("Points are only awarded if supporting data is provided.")
                    for key, q_text in questions_B.items():
                        is_checked = st.checkbox(q_text, value=rec_B.get(key, False), key=key)
                        data_provided = st.text_area(f"Evidence/Data for Q above:", height=50, key=f"data_{key}", value=rec_data if rec_B.get(key) else "")
                        if is_checked and data_provided.strip():
                            score_B += WEIGHTS['product_B'][key]
                        elif is_checked and not data_provided.strip():
                            st.warning("Provide evidence to receive points.", icon="⚠️")
                    st.session_state.scores['B'] = score_B
                    st.write(f"**Score B: {score_B} / 11**")
                
                if st.button("Calculate Recommendation"): set_stage(207)

            elif st.session_state.stage == 207:
                score_a, score_b = st.session_state.scores['A'], st.session_state.scores['B']
                score_a_high = st.session_state.scores['A'] >= HIGH_THRESHOLD
                score_b_high = st.session_state.scores['B'] >= HIGH_THRESHOLD
                outcome_key = ''
                if score_a_high and score_b_high: outcome_key = 'product_endorsed'
                elif not score_a_high and score_b_high: outcome_key = 'flag_review'
                else: outcome_key = 'product_led'
                display_result(outcome_key)

# --- App Execution ---
if check_password():
    run_app()
