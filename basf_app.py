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

# --- Data Libraries (Fully Restored & Updated for V3 Logic) ---
# NOTE: Demos have been re-mapped to the new V3 stage numbering and logic.
# No demos have been removed.
DEMO_DATA = {
    # --- Corporate Path Demos (Re-mapped) ---
    # Path: Commercial -> Corporate -> Ownership (Wholly-Owned) -> Not Acquisition -> Risk (No) -> Legal (No) -> Resources (Yes) -> Scorecard
    "chemicals": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a1': True, 'a2': True, 'a4': True, 'a5': True}, 'score_B_checks': {}, 'rationale': "As the core engine of BASF, its contribution is maximum. Its entire value comes from being BASF, so its need for market distinction is minimal."}},
    "chemovator": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a1': True, 'a2': True, 'a3': True}, 'score_B_checks': {'b2': True, 'b3': True}, 'rationale': "As a key pillar of BASF's innovation strategy, its contribution is high. Its entire purpose requires a distinct identity to attract new talent and foster an agile culture, so its distinction need is also high."}},
    "newbiz": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a3': True}, 'score_B_checks': {'b2': True, 'b3': True, 'b4': True}, 'rationale': "As an exploratory venture, its contribution is not yet core to strategy but it has a very high need for market distinction to succeed in a new field."}},
    "coatings": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a1': True, 'a3': True, 'a5': True}, 'score_B_checks': {'b3': True, 'b4': True}, 'rationale': "As a key growth pillar competing with pure-players, it is strategically vital but needs its own brand to win."}},
    "ecms": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a2': True, 'a3': True, 'a4': True}, 'score_B_checks': {'b3': True, 'b4': True}, 'rationale': "As a sustainability-focused growth pillar, it's highly strategic but needs a distinct identity for its specialized market."}},
    "care360": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {'a2': True, 'a4': True}, 'score_B_checks': {}, 'rationale': "As a solutions platform, its entire purpose is to showcase the power of the masterbrand. It needs to be the embodiment of BASF, not distinct from it."}},
    
    # --- Corporate Path Off-Ramp Demos (Re-mapped) ---
    "newco": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 0}, 'stage1.2': {'index': 1}, 'rationale': "This demo assumes a standard acquisition of a company with a valuable, positive brand equity that should be integrated."},
    "basfsonatrachpropanchem": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 2}, 'stage1.3': {'index': 0}, 'stage3': {'index': 0, 'rationale': "As a Joint Venture, the branding is often defined in the legal agreement that formed the company. This demo assumes a legal directive exists, triggering that off-ramp."}},
    "insight360": {'path': 'corporate', 'stage0.5': {'index': 1, 'rationale': "This is a tool for internal employees, so it's considered Non-commercial. The tool provides an immediate off-ramp to a BASF-Led outcome."}}, # Re-mapped to new Non-commercial path
    "anniversaries": {'path': 'corporate', 'stage0.5': {'index': 1, 'rationale': "This is a temporary campaign, not a permanent brand, so it's considered Non-commercial. The tool provides an immediate off-ramp to a BASF-Led outcome."}}, # Re-mapped to new Non-commercial path

    # --- Stress-Test Demos (Re-mapped) ---
    "polyweld800business": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 1}, 'stage3': {'index': 1}, 'stage4': {'index': 1}, 'stage5': {'score_A_checks': {}, 'score_B_checks': {}, 'rationale': "This legacy business is no longer part of the 'Winning Ways' strategy and competes on price, not brand. Both its strategic contribution and market distinction needs are low."}},
    "extractmax": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 1}, 'stage2': {'index': 0, 'rationale': "Due to its use in a controversial industry, this product carries a significant reputational risk that could harm the masterbrand, triggering the risk-insulation off-ramp."}},
    "oldcheminc": {'path': 'corporate', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 0}, 'stage1': {'index': 1}, 'stage1.1': {'index': 0}, 'stage1.2': {'index': 0, 'rationale': "This demo assumes the acquired brand has a known negative reputation, which would be a liability for BASF to inherit, triggering a 'retire & rebrand' recommendation."}},

    # --- Product Path Demos (Re-mapped) ---
    "glasurit": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 1}, 'stage202.1': {'index': 1}, 'stage203': {'index': 1}, 'stage204': {'index': 1}, 'stage205': {'index': 1}, 'stage206': {'score_A_checks': {'pa1': True, 'pa2': True, 'pa3': True, 'pa4': True}, 'score_B_checks': {'pb1': True, 'pb2': True}, 'data_mandate': "Data shows Glasurit competes directly against other powerful consumer-facing refinish brands like Axalta/PPG and needs its own identity to speak to body shop owners and maintain its premium position.", 'rationale': "As a cornerstone of the Coatings division, its contribution is high. It competes in a distinct B2B2C market against strong brand players, giving it a high need for distinction."}},
    "ultramid": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 1}, 'stage202.1': {'index': 1}, 'stage203': {'index': 1}, 'stage204': {'index': 1}, 'stage205': {'index': 1}, 'stage206': {'score_A_checks': {'pa1': True, 'pa2': True, 'pa4': True, 'pa5': True}, 'score_B_checks': {}, 'data_mandate': "N/A - No distinction needed.", 'rationale': "As a workhorse ingredient brand, its contribution is high. Its value is derived from being a trusted BASF product, so its need for market distinction is low."}},
    
    # --- Product Path Stress-Tests (Re-mapped) ---
    "noresourceproduct": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 1}, 'stage202.1': {'index': 1}, 'stage203': {'index': 1}, 'stage204': {'index': 1}, 'stage205': {'index': 0, 'rationale': "This demo shows what happens when a product team indicates they do not have the dedicated budget to support a distinct brand."}},
    "jvproduct": {'path': 'product', 'stage0.5': {'index': 0}, 'stage0.6': {'index': 1}, 'stage201': {'index': 1}, 'stage202': {'index': 2}, 'stage202.2': {'index': 1, 'rationale': "This demo shows the outcome for a product that belongs to a non-wholly-owned entity like a Joint Venture. The product must follow the parent entity's branding."}}
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


# --- WEIGHTING SYSTEM (V3 Updated) ---
WEIGHTS = {
    'corporate_A': {'a1': 3, 'a2': 3, 'a3': 2, 'a4': 2, 'a5': 1},
    'corporate_B': {'b1': 3, 'b2': 2, 'b3': 2, 'b4': 2, 'b5': 1}, # Updated per V3 scorecard
    'product_A': {'pa1': 3, 'pa2': 3, 'pa3': 2, 'pa4': 2, 'pa5': 1},
    'product_B': {'pb1': 3, 'pb2': 3, 'pb3': 2, 'pb4': 2, 'pb5': 1}
}
HIGH_THRESHOLD = 6

# --- INTERACTIVE IMAGE VIEWER FUNCTION (Unchanged) ---
def display_interactive_image(image_path: str):
    try:
        image_bytes = Path(image_path).read_bytes()
        encoded_image = base64.b64encode(image_bytes).decode()
        image_html_src = f"data:image/png;base64,{encoded_image}"
    except FileNotFoundError:
        st.error(f"Image file not found at '{image_path}'. Make sure it's in the same directory as the script.")
        return

    html_code = f'''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.3/viewer.min.css" />
    <div id="image-container">
      <img id="flowchart-image" src="{image_html_src}" alt="Brand Compass Flowchart" style="max-width: 100%; cursor: zoom-in;">
    </div>
    <p style="text-align:center; color:grey;">Click image to open interactive viewer</p>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.3/viewer.min.js"></script>
    <script>
      const viewer = new Viewer(document.getElementById('flowchart-image'), {{
        inline: false,
        toolbar: {{
            zoomIn: 1, zoomOut: 1, oneToOne: 1, reset: 1, prev: 0, 
            play: {{ show: 0 }},
            next: 0, rotateLeft: 1, rotateRight: 1, flipHorizontal: 1, flipVertical: 1,
        }},
      }});
    </script>
    '''
    st.components.v1.html(html_code, height=400)


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

    # --- CORRECTED RESET FUNCTION ---
    def reset_app_callback():
        """
        Clears all session state variables except for the password flag
        and explicitly sets the stage to 0. Designed to be used as a
        button callback.
        """
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
        # Use the corrected callback function here
        st.button("Evaluate Another Entity", on_click=reset_app_callback)
    
    st.title("🧭 The BASF Brand Compass")
    if st.session_state.stage == 0:
        # --- HOME PAGE (Unchanged) ---
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
        stress_demos = {"PolyWeld 800 Business": "polyweld800business", "ExtractMax": "extractmax", "OldChem Inc.": "oldcheminc", "No-Resource Product": "noresourceproduct", "JV Product": "jvproduct"}
        cols = st.columns(len(stress_demos))
        for i, (name, key) in enumerate(stress_demos.items()):
            with cols[i]:
                if st.button(name, key=key, use_container_width=True): start_evaluation(name, is_demo=True, demo_key=key)

        with st.expander("View the Brand Compass Flowchart"):
            display_interactive_image("flowchart.png") 

    elif st.session_state.stage == 0.5:
        # --- NEW STRATEGIC ROUTER (V3) ---
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        st.subheader("Strategic Router")
        st.write("**What is the purpose of the entity being evaluated?**")
        
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
        # --- NEW NATURE OF ENTITY ROUTER (V3) ---
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        st.subheader("Strategic Router")
        st.write("**What is the nature of the entity?**")
        st.caption("This routes the entity to the correct evaluation path. Corporate entities have access to the full strategic spectrum, while products, services, or solutions follow a more constrained path.")
        
        path_options = ["Corporate Entity (e.g., a company, JV, business unit)", "Product, Service, or Solution"]
        
        demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage0.6', {})
        rec_index = demo_data.get('index')
        
        path_choice = st.radio("Select the entity type:", path_options, index=rec_index, key="path_router")
        
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
            # --- CORPORATE PATH (V3 RESTRUCTURED) ---
            st.header(f"Evaluating: *{st.session_state.entity_name}* (Corporate Path)")
            
            # --- STAGE 1: OWNERSHIP ---
            if st.session_state.stage == 1:
                st.subheader("Circuit Breaker 1: Ownership")
                options = ["Partner / Distributor", "Wholly Owned", "Joint Venture"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1', {})
                choice = st.radio("What is the ownership structure?", options, index=demo_data.get('index'))
                if st.button("Proceed"):
                    if choice == options[0]: display_result('follow_partner_guidelines')
                    elif choice == options[1]: set_stage(1.1)
                    else: set_stage(1.3)
            
            # --- STAGE 1.1: ACQUISITION CHECK ---
            elif st.session_state.stage == 1.1:
                st.subheader("Circuit Breaker 1: Ownership")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.1', {})
                choice = st.radio("Is it an acquisition?", options, index=demo_data.get('index'))
                if st.button("Proceed"):
                    if choice == "Yes": set_stage(1.2)
                    else: set_stage(2) # Skip to Risk Profile
            
            # --- STAGE 1.2: NEGATIVE EQUITY CHECK ---
            elif st.session_state.stage == 1.2:
                st.subheader("Circuit Breaker 1: Ownership")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.2', {})
                choice = st.radio("Does the acquired brand have significant negative equity?", options, index=demo_data.get('index'))
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('retire_rebrand')
                    else: set_stage(2) # Skip to Risk Profile

            # --- STAGE 1.3: JOINT VENTURE CHECK ---
            elif st.session_state.stage == 1.3:
                st.subheader("Circuit Breaker 1: Ownership")
                options = ["Majority (+50%)", "Minority (-50%)"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.3', {})
                choice = st.radio("What is BASF's equity share?", options, index=demo_data.get('index'))
                if st.button("Proceed"):
                    if choice == options[1]: display_result('independent_minority')
                    else: set_stage(2) # Skip to Risk Profile

            # --- STAGE 2: RISK PROFILE ---
            elif st.session_state.stage == 2:
                st.subheader("Circuit Breaker 2: Risk Profile")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage2', {})
                choice = st.radio("Does it have the potential to create negative reputation impact for BASF?", options, index=demo_data.get('index'))
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('independent_risk')
                    else: set_stage(3)

            # --- STAGE 3: LEGAL DIRECTIVES ---
            elif st.session_state.stage == 3:
                st.subheader("Circuit Breaker 3: Legal Directives")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage3', {})
                choice = st.radio("Are there any pre-existing legal or contractual requirements that dictate the go-to-market strategy or brand identity?", options, index=demo_data.get('index'))
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('legal_directive')
                    else: set_stage(4)

            # --- STAGE 4: RESOURCES ---
            elif st.session_state.stage == 4:
                st.subheader("Circuit Breaker 4: Resources")
                options = ["No", "Yes"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage4', {})
                choice = st.radio("Will it have dedicated and approved resources to support multi-year identity and marketing efforts?", options, index=demo_data.get('index'))
                if st.button("Proceed"):
                    if choice == "No": display_result('flag_review')
                    else: set_stage(5)

            # --- STAGE 5: CORPORATE SCORECARD (V3 UPDATED) ---
            elif st.session_state.stage == 5:
                st.subheader("Strategic Scorecard")
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage5', {})
                rec_A = demo_data.get('score_A_checks', {})
                rec_B = demo_data.get('score_B_checks', {})

                questions_A = { 'a1': 'Corporate Business Strategy: Is it a cornerstone entity for our corporate strategy and ambition?', 'a2': 'Does it directly deliver on a key corporate initiative or impact an important KPI?', 'a3': 'Future Value: Is it a strategically designed to win in a distinct market, new segment or business model?', 'a4': 'Brand Character: Does it strongly support or demonstrate our desired brand positioning?', 'a5': 'Connection to Core: Does it operate within an established business segment linked to BASF\'s core capabilities?' }
                questions_B = { 'b1': 'BASF reputation: Is there a known negative perception of the BASF brand for the audience this entity targets?', 'b2': 'Category: Does this entity operate in a market defined by distinct expectations and conventions that the BASF brand may not be well suited for?', 'b3': 'Competitors: Does this entity compete primarily with specialised "pure-players" with go-to-market approaches tailored to the category?', 'b4': 'Customers: Does this entity need to appeal directly to end consumers who need to be engaged through highly specific consumer codes?', 'b5': 'Value Proposition: Does this entity have a unique way of working, relative to other BASF entities, that needs to be highlighted as part of its unique' }

                score_A, score_B = 0, 0
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Part A: Strategic Contribution**")
                    for key, q_text in questions_A.items():
                        if st.checkbox(q_text, value=rec_A.get(key, False), key=key): score_A += WEIGHTS['corporate_A'][key]
                    st.session_state.scores['A'] = score_A
                    st.write(f"**Score A: {score_A} / 11**")
                
                with col2:
                    st.info("**Part B: Market Distinction**")
                    for key, q_text in questions_B.items():
                        if st.checkbox(q_text, value=rec_B.get(key, False), key=key): score_B += WEIGHTS['corporate_B'][key]
                    st.session_state.scores['B'] = score_B
                    st.write(f"**Score B: {score_B} / 10**") # V3 Total is 10
                
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Calculate Recommendation"): set_stage(6)

            # --- STAGE 6: CORPORATE RESULT LOGIC (Unchanged) ---
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
            # --- PRODUCT PATH (V3 RESTRUCTURED) ---
            st.header(f"Evaluating: *{st.session_state.entity_name}* (Product Path)")

            # --- STAGE 201: GOVERNANCE ---
            if st.session_state.stage == 201:
                st.subheader("Circuit Breaker 1: Governance")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage201', {})
                choice = st.radio("Will it be deployed and managed by an Independent business that currently does not use the BASF brand?", options, index=demo_data.get('index'))
                if st.button("Proceed"):
                    if choice == "Yes": display_result('not_governed_by_basf')
                    else: set_stage(202)

            # --- STAGE 202: OWNERSHIP ---
            elif st.session_state.stage == 202:
                st.subheader("Circuit Breaker 2: Ownership")
                options = ["Partner / Distributor", "Wholly Owned", "Joint Venture"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202', {})
                choice = st.radio("What is the ownership structure?", options, index=demo_data.get('index'))
                if st.button("Proceed"):
                    if choice == options[0]: display_result('follow_partner_guidelines')
                    elif choice == options[1]: set_stage(202.1)
                    else: set_stage(202.2)

            # --- STAGE 202.1: ACQUISITION CHECK ---
            elif st.session_state.stage == 202.1:
                st.subheader("Circuit Breaker 2: Ownership")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202.1', {})
                choice = st.radio("Is it an acquisition?", options, index=demo_data.get('index'))
                if st.button("Proceed"):
                    if choice == "Yes": set_stage(202.3)
                    else: set_stage(203)

            # --- STAGE 202.2: JOINT VENTURE CHECK ---
            elif st.session_state.stage == 202.2:
                st.subheader("Circuit Breaker 2: Ownership")
                st.info("Products belonging to a Joint Venture must follow the branding of the parent JV entity.")
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Show Recommendation"):
                    display_result('evaluate_parent_entity')

            # --- STAGE 202.3: NEGATIVE EQUITY CHECK ---
            elif st.session_state.stage == 202.3:
                st.subheader("Circuit Breaker 2: Ownership")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202.3', {})
                choice = st.radio("Does the acquired brand have significant negative equity?", options, index=demo_data.get('index'))
                if st.button("Proceed"):
                    if choice == "Yes": display_result('retire_rebrand')
                    else: set_stage(203)

            # --- STAGE 203: RISK PROFILE ---
            elif st.session_state.stage == 203:
                st.subheader("Circuit Breaker 3: Risk Profile")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage203', {})
                choice = st.radio("Does it have the potential to create negative reputation impact for BASF?", options, index=demo_data.get('index'))
                if st.button("Proceed"):
                    if choice == "Yes": display_result('independent_risk')
                    else: set_stage(204)

            # --- STAGE 204: LEGAL DIRECTIVES ---
            elif st.session_state.stage == 204:
                st.subheader("Circuit Breaker 4: Legal Directives")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage204', {})
                choice = st.radio("Are there any pre-existing legal or contractual requirements that dictate the go-to-market strategy or brand identity?", options, index=demo_data.get('index'))
                if st.button("Proceed"):
                    if choice == "Yes": display_result('legal_directive')
                    else: set_stage(205)

            # --- STAGE 205: RESOURCES ---
            elif st.session_state.stage == 205:
                st.subheader("Circuit Breaker 5: Resources")
                options = ["No", "Yes"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage205', {})
                choice = st.radio("Will it have dedicated and approved resources to support multi-year identity and marketing efforts?", options, index=demo_data.get('index'))
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                if st.button("Proceed"):
                    if choice == "No": display_result('insufficient_resources')
                    else: set_stage(206)

            # --- STAGE 206: PRODUCT SCORECARD (V3 UPDATED) ---
            elif st.session_state.stage == 206:
                st.subheader("High-Rigor Product Scorecard")
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage206', {})
                rec_A = demo_data.get('score_A_checks', {})
                rec_B = demo_data.get('score_B_checks', {})
                rec_data = demo_data.get('data_mandate', "")

                questions_A = { 'pa1': 'Corporate Strategy Contribution: Is this product, service or solution a cornerstone of a strategic BASF business initiative?', 'pa2': 'Equity Building: Does this offer create a significant positive "halo effect" or reputation impact for the BASF umbrella brand?', 'pa3': 'Market Opportunity: Does this offer provide access to a new, strategically important customer segment and/or market?', 'pa4': 'Commercial Potential: Does this offer have proven high revenue and/or margin potential?', 'pa5': 'Future Value: Does this offer represent a breakthrough technology or innovation?' }
                questions_B = { 'pb1': 'Portfolio Clarity: Does this offer need a distinct identity to prevent portfolio confusion/cannibalisation?', 'pb2': 'Customers: Does this entity need to appeal directly to end consumers who need to be engaged through highly specific consumer codes?', 'pb3': 'Competitors: Does this offer compete against other specialised "pure-player" or consumer brands where \'BASF\' is a disadvantage?', 'pb4': 'Marketing: Does this offer require a unique, agile, or specialised go-to-market approach (e.g., e-commerce, different sales)?', 'pb5': 'BASF reputation: Does data prove this offer needs differentiation from the BASF masterbrand to win?' }
                
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

            # --- STAGE 207: PRODUCT RESULT LOGIC ---
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
