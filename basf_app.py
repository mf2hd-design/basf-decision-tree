import streamlit as st
import base64
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="BASF Brand Compass",
    page_icon="🧭",
    layout="centered"
)

# --- Password Protection Logic (Robust Version) ---
def check_password():
    """Returns `True` if the user is logged in."""
    def password_entered():
        # This password is for demonstration purposes.
        # In a real-world scenario, use st.secrets for secure password management.
        if st.session_state.get("password") == "FFxBASF2025":
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

# --- Data Libraries (Fully Restored & Updated for V3 Logic with Complete Demo Paths) ---
DEMO_DATA = {
    # --- Corporate Path Demos (Paths to Scorecard are now complete) ---
    "chemicals": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a1': True, 'a2': True, 'a4': True, 'a5': True}, 'score_B_checks': {}, 'rationale': "As the core engine of BASF, its contribution is maximum. Its entire value comes from being BASF, so its need for market distinction is minimal."}},
    "chemovator": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a1': True, 'a2': True, 'a3': True}, 'score_B_checks': {'b2': True, 'b3': True}, 'rationale': "As a key pillar of BASF's innovation strategy, its contribution is high. Its entire purpose requires a distinct identity to attract new talent and foster an agile culture, so its distinction need is also high."}},
    "newbiz": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a3': True}, 'score_B_checks': {'b2': True, 'b3': True, 'b4': True}, 'rationale': "As an exploratory venture, its contribution is not yet core to strategy but it has a very high need for market distinction to succeed in a new field."}},
    "coatings": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a1': True, 'a3': True, 'a5': True}, 'score_B_checks': {'b3': True, 'b4': True}, 'rationale': "As a key growth pillar competing with pure-players, it is strategically vital but needs its own brand to win."}},
    "ecms": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a2': True, 'a3': True, 'a4': True}, 'score_B_checks': {'b3': True, 'b4': True}, 'rationale': "As a sustainability-focused growth pillar, it's highly strategic but needs a distinct identity for its specialized market."}},
    "care360": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a2': True, 'a4': True}, 'score_B_checks': {}, 'rationale': "As a solutions platform, its entire purpose is to showcase the power of the masterbrand. It needs to be the embodiment of BASF, not distinct from it."}},
    
    # --- Corporate Path Off-Ramp Demos (Paths are now complete) ---
    "newco": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 0}, 'stage1.2': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {}, 'score_B_checks': {}, 'rationale': "This demo assumes a standard acquisition of a company with a valuable, positive brand equity. It should pass all circuit breakers and be evaluated on the scorecard."}},
    "basfsonatrachpropanchem": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 2}, 'stage1.3': {'index': 0}, 'stage2': {'index': 1}, 'stage3': {'index': 0, 'rationale': "As a Joint Venture, the branding is often defined in the legal agreement. This demo assumes a legal directive exists, triggering that off-ramp after passing the risk check."}},
    "insight360": {'path': 'corporate', 'stage0.5': {'index': 1, 'rationale': "This is a tool for internal employees, so it's considered Non-commercial. The tool provides an immediate off-ramp to a BASF-Led outcome."}},
    "anniversaries": {'path': 'corporate', 'stage0.5': {'index': 1, 'rationale': "This is a temporary campaign, not a permanent brand, so it's considered Non-commercial. The tool provides an immediate off-ramp to a BASF-Led outcome."}},

    # --- Stress-Test Demos (Paths are now complete) ---
    "polyweld800business": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {}, 'score_B_checks': {}, 'rationale': "This legacy business is no longer part of the 'Winning Ways' strategy and competes on price, not brand. Both its strategic contribution and market distinction needs are low."}},
    "extractmax": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 0, 'rationale': "Due to its use in a controversial industry, this product carries a significant reputational risk that could harm the masterbrand, triggering the risk-insulation off-ramp."}},
    "oldcheminc": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 0}, 'stage1.2': {'index': 0, 'rationale': "This demo assumes the acquired brand has a known negative reputation, which would be a liability for BASF to inherit, triggering a 'retire & rebrand' recommendation."}},

    # --- Product Path Demos (Paths are now complete) ---
    "glasurit": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 1}, 'stage202.1': {'index': 1}, 'stage203': {'index': 1}, 'stage204': {'index': 1}, 'stage205': {'index': 1}, 'stage206': {'score_A_checks': {'pa1': True, 'pa2': True, 'pa3': True, 'pa4': True}, 'score_B_checks': {'pb1': True, 'pb2': True}, 'data_mandate': "Data shows Glasurit competes directly against other powerful consumer-facing refinish brands like Axalta/PPG and needs its own identity to speak to body shop owners and maintain its premium position.", 'rationale': "As a cornerstone of the Coatings division, its contribution is high. It competes in a distinct B2B2C market against strong brand players, giving it a high need for distinction."}},
    "ultramid": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 1}, 'stage202.1': {'index': 1}, 'stage203': {'index': 1}, 'stage204': {'index': 1}, 'stage205': {'index': 1}, 'stage206': {'score_A_checks': {'pa1': True, 'pa2': True, 'pa4': True, 'pa5': True}, 'score_B_checks': {}, 'data_mandate': "N/A - No distinction needed.", 'rationale': "As a workhorse ingredient brand, its contribution is high. Its value is derived from being a trusted BASF product, so its need for market distinction is low."}},
    
    # --- Product Path Stress-Tests (Paths are now complete) ---
    "noresourceproduct": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 1}, 'stage202.1': {'index': 1}, 'stage203': {'index': 1}, 'stage204': {'index': 1}, 'stage205': {'index': 0, 'rationale': "This demo shows what happens when a product team indicates they do not have the dedicated budget to support a distinct brand."}},
    "jvproduct": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 2, 'rationale': "This demo shows the outcome for a product that belongs to a non-wholly-owned entity like a Joint Venture. The product must follow the parent entity's branding."}}
}


RESULT_DATA = {
    # Corporate Path Outcomes
    'basf_led': {'recommendation': "BASF-Led", 'rationale': "This entity's primary purpose is to be a direct expression of the BASF masterbrand, is non-commercial, or lacks the resources for a distinct identity. Its value is maximized by being an integral part of BASF.", 'activation_text': "This means we don't create a separate brand. The entity is branded simply as 'BASF [Entity Name]'. It lives on the main BASF website and is sold by the BASF sales team, reinforcing the power and innovation of the masterbrand.", 'examples': "Chemicals Division, Internal Tools"},
    'endorsed_level1': {'recommendation': "BASF-Endorsed (Level 1: Co-Branded Lockup)", 'rationale': "This entity is a strategically critical pillar but requires its own distinct identity to win. The recommendation is a tight, explicit endorsement to transfer maximum trust from the masterbrand.", 'activation_text': "This triggers the **Co-Branded Lockup** playbook. The entity will have its own distinct brand identity but must use a mandatory visual co-branding system with the BASF logo. This provides the highest level of explicit backing and is reserved for our most important strategic ventures.", 'examples': "Chemovator GmbH"},
    'endorsed_level2': {'recommendation': "BASF-Endorsed (Level 2: Prominent Verbal Endorsement)", 'rationale': "This entity is an important, established brand that needs its own space but gains significant credibility and value from an explicit BASF link.", 'activation_text': "This triggers the **Prominent Verbal Endorsement** playbook. The brand operates with its own identity, supported by the classic 'powered by BASF' or 'A BASF Company' tagline. This provides a strong, clear connection that builds trust without a full visual lockup.", 'examples': "Coatings Division Brands"},
    'endorsed_level3': {'recommendation': "BASF-Endorsed (Level 3: Distant Verbal Endorsement)", 'rationale': "This entity is an exploratory venture that needs maximum independence. A subtle, distant link provides a 'halo' of quality while insulating the masterbrand from risk.", 'activation_text': "This triggers the **Distant Endorsement** playbook. The brand operates with full independence. The connection to BASF is strategic and not part of the primary brand identity. It is typically mentioned in non-consumer-facing contexts like 'About Us' sections, corporate reports, or investor relations.", 'examples': "NewBiz (Hypothetical)"},
    'flag_review': {'recommendation': "Flag for Strategic Review", 'rationale': "This entity's profile indicates a misalignment. This could be due to low strategic importance, a lack of resources for a needed brand, or other factors identified in the circuit breakers. This is a business issue, not just a branding problem.", 'activation_text': "This is not a branding recommendation but a business flag. The entity's situation warrants a formal business review to determine its future within the portfolio before any branding decisions are made.", 'examples': "PolyWeld 800 Business"},
    # Product Path Outcomes
    'product_led': {'recommendation': "BASF-Led (Product Level)", 'rationale': "This product's value is maximized by leveraging the full trust and equity of the BASF masterbrand. There is no data-backed business case for the cost and complexity of a distinct identity.", 'activation_text': "The recommendation is to use the standard **'BASF Productname®'** lockup. This approach ensures market clarity, reinforces BASF's quality promise, and provides the strongest return on investment. Please consult the BASF Brand Portal for the correct templates and usage rules.", 'examples': "Ultramid®"},
    'product_endorsed': {'recommendation': "BASF-Endorsed (Product Level)", 'rationale': "This product is a cornerstone of a divisional strategy and has a proven, data-backed need for a distinct identity to win in its specific market.", 'activation_text': "This product has earned the right to a distinct brand identity. It must be supported by a mandatory, explicit endorsement (e.g., 'powered by BASF'). A full business case and brand plan must be submitted to the divisional leadership for approval before development.", 'examples': "Glasurit®"},
    'insufficient_resources': {'recommendation': "Flag for Review (Insufficient Resources)", 'rationale': "Building and sustaining a distinct brand requires significant, long-term investment. Without dedicated resources, a new brand identity cannot succeed and may damage the BASF brand through inconsistent application.", 'activation_text': "The entity does not have the required resources to support a distinct brand. This triggers a **Flag for Review**. A business decision must be made: either secure the necessary multi-year funding or default to a 'BASF-Led' branding approach to leverage the masterbrand's resources.", 'examples': "Any product without a dedicated brand budget"},
    'evaluate_parent_entity': {'recommendation': "Evaluate Parent Entity First", 'rationale': "A product's branding cannot be decided until its parent company's relationship to BASF is defined.", 'activation_text': "This product belongs to an entity that is not wholly-owned by BASF (e.g., a Joint Venture). Please use the **Corporate Path** in this tool to evaluate the parent corporate entity first. The branding of its products must follow the guidelines and endorsement level established for the parent company.", 'examples': "Products from a Joint Venture"},
    # General Outcomes
    'not_governed_by_basf': {'recommendation': "Not Governed by BASF Brand", 'rationale': "The entity is deployed and managed by an independent business that does not currently use the BASF brand.", 'activation_text': "This entity falls outside the governance of the BASF brand architecture. The recommendation is to treat it as 'Independent' or follow the specific branding guidelines of the business responsible for managing it. No further evaluation in this tool is needed.", 'examples': "A product created by an independent subsidiary like Wintershall Dea."},
    'legal_directive': {'recommendation': "Follow Legal Directive", 'rationale': "The branding for this entity is pre-determined by a binding legal or contractual agreement which must be followed.", 'activation_text': "The branding for this entity is dictated by a binding legal or contractual agreement. The primary action is to consult the specific legal documents (e.g., the Joint Venture agreement) and implement the branding exactly as specified. This overrides all other strategic considerations.", 'examples': "BASF SONATRACH PropanChem"},
    'independent_risk': {'recommendation': "Independent (for risk insulation)", 'rationale': "The entity has the potential to create significant negative reputation impact for BASF and must be strategically distanced from the masterbrand.", 'activation_text': "This means the entity must operate as a fully independent brand with no visible connection to BASF. This is a strategic decision to create a 'reputational firewall' and insulate the masterbrand from potential risk.\n\n**Maintaining the BASF Connection:** While this entity operates independently, it must adhere to BASF's non-negotiable core principles, including Safety & Compliance Standards, Code of Conduct, and Legal Transparency of Ownership.", 'examples': "ExtractMax"},
    'follow_partner_guidelines': {'recommendation': "Follow Partner/Distributor Guidelines", 'rationale': "As a third-party partner/distributor with no BASF equity stake, branding is governed by specific legal and brand guidelines.", 'activation_text': "The primary action is to consult the official 'Distributor Branding Guidelines' and engage with the Brand Consultancy team to ensure full compliance before using any BASF branding. This ensures consistency and protects both brands.", 'examples': "Third-Party Distributors"},
    'independent_minority': {'recommendation': "Independent (Minority-owned JV)", 'rationale': "As a minority stakeholder (<50% equity), BASF cannot enforce its brand identity. The JV must operate with its own distinct brand to ensure legal and market clarity.", 'activation_text': "This entity requires its own independent brand identity. BASF's involvement should be communicated strategically as an endorsement or partnership, guided by the terms of the Joint Venture agreement, rather than through direct branding.", 'examples': "Minority-stake Joint Ventures"},
    'retire_rebrand': {'recommendation': "Independent (Retire & Rebrand)", 'rationale': "The acquired brand has significant negative equity, making its association a liability. The recommendation is to make it independent by retiring the name and transitioning customers to a new or existing BASF brand.", 'activation_text': "This means the acquired brand identity will be retired. A formal plan must be created to migrate customers and assets to a new or existing BASF brand, thereby making the business independent of the problematic legacy name.\n\n**Maintaining the BASF Connection:** While this entity operates independently, it must adhere to BASF's non-negotiable core principles, including Safety & Compliance Standards, Code of Conduct, and Legal Transparency of Ownership.", 'examples': "OldChem Inc."}
}


# --- WEIGHTING SYSTEM (CORRECTED) ---
WEIGHTS = {
    'corporate_A': {'a1': 3, 'a2': 3, 'a3': 2, 'a4': 2, 'a5': 1},
    'corporate_B': {'b1': 3, 'b2': 3, 'b3': 2, 'b4': 2, 'b5': 1}, # Corrected: b2 is now 3 points
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
        
        # --- STRESS TEST DEMOS WITH EXPLANATIONS ---
        stress_demos = {
            "PolyWeld 800 Business": {
                "key": "polyweld800business",
                "caption": "Tests a legacy business with low strategic contribution, leading to a 'Flag for Review' outcome."
            },
            "ExtractMax": {
                "key": "extractmax",
                "caption": "Tests the reputational risk circuit breaker for a profitable but controversial entity."
            },
            "OldChem Inc.": {
                "key": "oldcheminc",
                "caption": "Tests the acquisition path for a company with negative brand equity."
            },
            "No-Resource Product": {
                "key": "noresourceproduct",
                "caption": "Tests the product path for an entity that lacks a dedicated multi-year brand budget."
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

        # --- EXPANDER WITH ROBUST PDF DOWNLOAD BUTTON ---
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
                st.caption("Click to download the full PDF. Most browsers will open it in a new tab for viewing.")
            except FileNotFoundError:
                st.error("File not found: 'document.pdf'. Please ensure the PDF is in the same directory as the script and restart the app.")


    elif st.session_state.stage == 0.5:
        # --- STRATEGIC ROUTER WITH IMPROVED EXPLANATIONS ---
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        st.subheader("Strategic Router")
        st.markdown("""
        **What is the purpose of the entity being evaluated?**

        This is the most important first step. It separates market-facing businesses from internal or marketing activities.
        
        *   **Commercial:** Choose this if the entity is **market-facing and has its own Profit & Loss (P&L)**. It directly sells products or services to customers.
            *   *Examples: A business unit, a subsidiary company, a product line.*
        
        *   **Non-commercial:** Choose this for **any other activity, even if it supports commercial goals.** These are typically cost centers that do not have their own P&L.
            *   *Examples: Marketing campaigns, events, trade fairs, internal initiatives, R&D projects, think tanks.*
        """)
        
        path_options = ["Commercial", "Non-commercial"]
        demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage0.5', {})
        rec_index = demo_data.get('index')
        
        st.markdown("---")
        path_choice = st.radio("Select the entity's purpose:", path_options, index=rec_index, key="purpose_router")
        
        if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")

        if st.button("Proceed"):
            if path_choice == path_options[1]: # Non-commercial
                display_result('basf_led')
            else: # Commercial
                set_stage(0.6)

    elif st.session_state.stage == 0.6:
        # --- NEW NATURE OF ENTITY ROUTER (V3) ---
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        st.subheader("Strategic Router")
        st.write("**What is the nature of the entity?**")
        st.caption("This routes the entity to the correct evaluation path. Corporate entities (like companies or business units) have different strategic considerations than Products, Services, or Solutions.")
        
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
        # --- ALL OTHER STAGES ---
        if st.session_state.path_type == 'corporate':
            # --- CORPORATE PATH (V3 RESTRUCTURED WITH SIMPLIFIED LANGUAGE) ---
            st.header(f"Evaluating: *{st.session_state.entity_name}* (Corporate Path)")
            
            if st.session_state.stage == 1:
                st.subheader("Circuit Breaker 1: Ownership")
                st.write("**What is the ownership structure?**")
                st.caption("This step checks the legal relationship to BASF, which decides many branding rules.")
                options = ["Partner / Distributor", "Wholly Owned", "Joint Venture"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1', {})
                choice = st.radio("Select ownership structure:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == options[0]: display_result('follow_partner_guidelines')
                    elif choice == options[1]: set_stage(1.1)
                    else: set_stage(1.3)
            
            elif st.session_state.stage == 1.1:
                st.subheader("Circuit Breaker 1: Ownership")
                st.write("**Is it an acquisition?**")
                st.caption("Answering 'Yes' helps determine how to handle the brand name of the company that was purchased.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.1', {})
                choice = st.radio("Select if it is an acquisition:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": set_stage(1.2)
                    else: set_stage(2)
            
            elif st.session_state.stage == 1.2:
                st.subheader("Circuit Breaker 1: Ownership")
                st.write("**Does the acquired brand have a bad reputation?**")
                st.caption("If a brand has a known negative history, we must retire it to protect BASF's reputation.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.2', {})
                choice = st.radio("Select if it has a bad reputation:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('retire_rebrand')
                    else: set_stage(2)

            elif st.session_state.stage == 1.3:
                st.subheader("Circuit Breaker 1: Ownership")
                st.write("**What is BASF's ownership share in the Joint Venture?**")
                st.caption("If BASF owns less than 50%, we cannot control its branding. The JV must legally have its own independent brand.")
                options = ["Majority (50% or more)", "Minority (less than 50%)"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.3', {})
                choice = st.radio("Select ownership share:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == options[1]: display_result('independent_minority')
                    else: set_stage(2)

            elif st.session_state.stage == 2:
                st.subheader("Circuit Breaker 2: Risk Profile")
                st.write("**Could it harm BASF's reputation?**")
                st.caption("If the entity is in a controversial industry or uses risky technology, it must be independent to protect the BASF masterbrand.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage2', {})
                choice = st.radio("Select if there is a potential for negative impact:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('independent_risk')
                    else: set_stage(3)

            elif st.session_state.stage == 3:
                st.subheader("Circuit Breaker 3: Legal Directives")
                st.write("**Does a legal contract already decide the brand?**")
                st.caption("For example, a joint venture agreement or brand license. If 'Yes', you must follow the contract. This tool's work is done.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage3', {})
                choice = st.radio("Select if a contract decides the brand:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('legal_directive')
                    else: set_stage(4)

            elif st.session_state.stage == 4:
                st.subheader("Circuit Breaker 4: Resources")
                st.write("**Does it have dedicated funding and a team for marketing?**")
                st.caption("A separate brand needs a multi-year budget to succeed. If there are no resources, it must be flagged for a business review.")
                options = ["No", "Yes"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage4', {})
                choice = st.radio("Select if resources are dedicated:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "No": display_result('flag_review')
                    else: set_stage(5)

            elif st.session_state.stage == 5:
                st.subheader("Strategic Scorecard")
                st.caption("The entity has passed all checks. Now, score its value to BASF and its need for a separate brand in the market.")
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage5', {})
                rec_A = demo_data.get('score_A_checks', {})
                rec_B = demo_data.get('score_B_checks', {})
                
                questions_A = { 
                    'a1': 'Is this a top priority for BASF\'s main business strategy?', 
                    'a2': 'Does it help achieve a major company goal or performance target (KPI)?', 
                    'a3': 'Is it designed to help BASF win in a new market, segment, or business model?', 
                    'a4': 'Does it strongly support or show our desired brand positioning?', 
                    'a5': "Does its business model rely on deep operational integration with BASF's core capabilities (e.g., shared expertise, platforms, or practices)?" 
                }
                questions_B = { 
                    'b1': 'Is there a known negative view of the BASF brand for this specific audience?', 
                    'b2': 'Does this market have special customer habits or rules that are different from BASF\'s usual markets?', 
                    'b3': 'Does it compete mainly with specialized, "pure-player" companies?', 
                    'b4': 'Does it need to sell directly to consumers using specific marketing language and styles?', 
                    'b5': 'Does it have a unique way of working that needs to be highlighted as part of its brand?' 
                }
                
                score_A, score_B = 0, 0
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Part A: Strategic Contribution**")
                    for key, q_text in questions_A.items():
                        if st.checkbox(q_text, value=rec_A.get(key, False), key=key): 
                            score_A += WEIGHTS['corporate_A'][key]
                        if key == 'a5':
                            st.caption("This clarifies the *operational model*, not its importance. A 'No' is common for agile, standalone ventures. A 'Yes' is typical for businesses that use shared resources. Both are valid strategies.")

                    st.session_state.scores['A'] = score_A
                    st.write(f"**Score A: {score_A} / 11**")
                with col2:
                    st.info("**Part B: Market Distinction**")
                    for key, q_text in questions_B.items():
                        if st.checkbox(q_text, value=rec_B.get(key, False), key=key): score_B += WEIGHTS['corporate_B'][key]
                    st.session_state.scores['B'] = score_B
                    st.write(f"**Score B: {score_B} / 11**")
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
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

        elif st.session_state.path_type == 'product':
            # --- PRODUCT PATH (V3 RESTRUCTURED WITH SIMPLIFIED LANGUAGE) ---
            st.header(f"Evaluating: *{st.session_state.entity_name}* (Product Path)")

            if st.session_state.stage == 201:
                st.subheader("Circuit Breaker 1: Governance")
                st.write("**Is it managed by an independent business that does not use the BASF brand?**")
                st.caption("This filters out things from outside the BASF brand system (e.g., a product from a subsidiary like Wintershall Dea). If 'Yes', this tool does not apply.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage201', {})
                choice = st.radio("Select if managed by an independent business:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('not_governed_by_basf')
                    else: set_stage(202)

            elif st.session_state.stage == 202:
                st.subheader("Circuit Breaker 2: Ownership")
                st.write("**What is the ownership structure?**")
                st.caption("This step checks the product's parent company to decide which branding rules to apply.")
                options = ["Partner / Distributor", "Wholly Owned", "Joint Venture"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202', {})
                choice = st.radio("Select ownership structure:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Proceed"):
                    if choice == options[0]: display_result('follow_partner_guidelines')
                    elif choice == options[1]: set_stage(202.1)
                    else: set_stage(202.2)

            elif st.session_state.stage == 202.1:
                st.subheader("Circuit Breaker 2: Ownership")
                st.write("**Is it an acquisition?**")
                st.caption("Answering 'Yes' helps determine how to handle the brand name of the product that was purchased.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202.1', {})
                choice = st.radio("Select if it is an acquisition:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": set_stage(202.3)
                    else: set_stage(203)

            elif st.session_state.stage == 202.2:
                st.subheader("Circuit Breaker 2: Ownership")
                st.write("Products from a Joint Venture must follow the parent company's brand.")
                st.caption("To find the correct brand for this product, please evaluate the parent Joint Venture company using the Corporate Path first.")
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Show Recommendation"):
                    display_result('evaluate_parent_entity')

            elif st.session_state.stage == 202.3:
                st.subheader("Circuit Breaker 2: Ownership")
                st.write("**Does the acquired brand have a bad reputation?**")
                st.caption("If a brand has a known negative history, we must retire it to protect BASF's reputation.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202.3', {})
                choice = st.radio("Select if it has a bad reputation:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('retire_rebrand')
                    else: set_stage(203)

            elif st.session_state.stage == 203:
                st.subheader("Circuit Breaker 3: Risk Profile")
                st.write("**Could it harm BASF's reputation?**")
                st.caption("If the product is used in a controversial industry, it must be independent to protect the BASF masterbrand.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage203', {})
                choice = st.radio("Select if there is a potential for negative impact:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('independent_risk')
                    else: set_stage(204)

            elif st.session_state.stage == 204:
                st.subheader("Circuit Breaker 4: Legal Directives")
                st.write("**Does a legal contract already decide the brand?**")
                st.caption("For example, a brand license agreement. If 'Yes', you must follow the contract. This tool's work is done.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage204', {})
                choice = st.radio("Select if a contract decides the brand:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('legal_directive')
                    else: set_stage(205)

            elif st.session_state.stage == 205:
                st.subheader("Circuit Breaker 5: Resources")
                st.write("**Does it have dedicated funding and a team for marketing?**")
                st.caption("A separate brand needs a multi-year budget to succeed. If there are no resources, it must be flagged for a business review.")
                options = ["No", "Yes"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage205', {})
                choice = st.radio("Select if resources are dedicated:", options, index=demo_data.get('index'), label_visibility="collapsed")
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Proceed"):
                    if choice == "No": display_result('insufficient_resources')
                    else: set_stage(206)

            elif st.session_state.stage == 206:
                st.subheader("High-Rigor Product Scorecard")
                st.caption("The product has passed all checks. Now, score its value to BASF and its need for a separate brand. All claims for market distinction must be supported by evidence.")
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage206', {})
                rec_A = demo_data.get('score_A_checks', {})
                rec_B = demo_data.get('score_B_checks', {})
                rec_data = demo_data.get('data_mandate', "")
                questions_A = { 'pa1': 'Is this a top priority for a major business division\'s strategy?', 'pa2': 'Does this create a positive "halo effect" for the main BASF brand?', 'pa3': 'Does this provide access to a new and important customer group or market?', 'pa4': 'Does it have proven high sales and/or profit margin?', 'pa5': 'Does it represent a breakthrough technology or innovation?' }
                questions_B = { 'pb1': 'Does data prove it needs its own brand to avoid confusing customers or competing with other BASF products ("cannibalisation")?', 'pb2': 'Does data prove it needs to appeal directly to consumers using specific marketing language and styles?', 'pb3': 'Does data prove it competes against specialized "pure-player" or consumer brands where "BASF" is a disadvantage?', 'pb4': 'Does it require a unique or specialized way of selling (e.g., e-commerce)?', 'pb5': 'Does data prove the BASF brand name is a negative factor for the target customer?' }
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
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Calculate Recommendation"): set_stage(207)

            elif st.session_state.stage == 207:
                score_a_high = st.session_state.scores['A'] >= HIGH_THRESHOLD
                score_b_high = st.session_state.scores['B'] >= HIGH_THRESHOLD
                outcome_key = ''
                if score_a_high and score_b_high: outcome_key = 'product_endorsed'
                elif not score_a_high and score_b_high: outcome_key = 'flag_review'
                else: outcome_key = 'product_led'
                display_result(outcome_key)

# --- App Execution with Password Check ---
if check_password():
    run_app()
