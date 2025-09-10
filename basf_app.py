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

# --- Data Libraries ---
DEMO_DATA = {
    "chemicals": {'path': 'corporate', 'stage1': {'index': 0, 'rationale': "The Chemicals division sells products to external customers."}, 'stage2': {'index': 0, 'rationale': "There are no specific legal or contractual requirements..."}, 'stage3': {'index': 0, 'rationale': "This is the core business and carries a standard risk profile."}, 'stage4': {'index': 0, 'rationale': "The division is a wholly-owned and created part of BASF."}, 'stage5': {'score_A_checks': {'a1': True, 'a2': True, 'a3': True, 'a4': True, 'a5': True}, 'score_B_checks': {'b1': False, 'b2': False, 'b3': False, 'b4': False, 'b5': False}, 'rationale': "As the core engine of BASF, its contribution is maximum. Its entire value comes from being BASF, so its need for market distinction is minimal."}},
    "chemovator": {'path': 'corporate', 'stage1': {'index': 0}, 'stage2': {'index': 0}, 'stage3': {'index': 0}, 'stage4': {'index': 0}, 'stage5': {'score_A_checks': {'a1': True, 'a2': True, 'a3': True, 'a4': False, 'a5': False}, 'score_B_checks': {'b1': True, 'b2': True, 'b3': True, 'b4': True, 'b5': False}, 'rationale': "As a key pillar of BASF's innovation strategy, its contribution is high. Its entire purpose requires a distinct identity to attract new talent and foster an agile culture, so its distinction need is also high."}},
    "newbiz": {'path': 'corporate', 'stage1': {'index': 0}, 'stage2': {'index': 0}, 'stage3': {'index': 0}, 'stage4': {'index': 0}, 'stage5': {'score_A_checks': {'a1': False, 'a2': False, 'a3': True, 'a4': False, 'a5': False}, 'score_B_checks': {'b1': True, 'b2': True, 'b3': False, 'b4': True, 'b5': True}, 'rationale': "As an exploratory venture, its contribution is not yet core to strategy but it has a very high need for market distinction to succeed in a new field."}},
    "polyweld800business": {'path': 'corporate', 'stage1': {'index': 0}, 'stage2': {'index': 0}, 'stage3': {'index': 0}, 'stage4': {'index': 0}, 'stage5': {'score_A_checks': {'a1': False, 'a2': False, 'a3': False, 'a4': False, 'a5': True}, 'score_B_checks': {'b1': False, 'b2': False, 'b3': False, 'b4': True, 'b5': False}, 'rationale': "This legacy business is no longer part of the 'Winning Ways' strategy and competes on price, not brand. Both its strategic contribution and market distinction needs are low."}},
    "glasurit": {'path': 'product', 'stage201': {'index': 1}, 'stage202': {'index': 0}, 'stage205': {'score_A_checks': {'pa1': True, 'pa2': True, 'pa3': True, 'pa4': True, 'pa5': False}, 'score_B_checks': {'pb1': True, 'pb2': True, 'pb3': True, 'pb4': False, 'pb5': False}, 'data_mandate': "Data shows Glasurit competes directly against other powerful consumer-facing refinish brands like Axalta/PPG and needs its own identity to speak to body shop owners and maintain its premium position.", 'rationale': "As a cornerstone of the Coatings division, its contribution is high. It competes in a distinct B2B2C market against strong brand players, giving it a high need for distinction."}},
    "ultramid": {'path': 'product', 'stage201': {'index': 1}, 'stage202': {'index': 0}, 'stage205': {'score_A_checks': {'pa1': True, 'pa2': True, 'pa3': False, 'pa4': True, 'pa5': True}, 'score_B_checks': {'pb1': False, 'pb2': False, 'pb3': False, 'pb4': False, 'pb5': False}, 'data_mandate': "N/A - No distinction needed.", 'rationale': "As a workhorse ingredient brand, its contribution is high. Its value is derived from being a trusted BASF product, so its need for market distinction is low."}},
    # Demos for circuit breakers
    "noresourceproduct": {'path': 'product', 'stage201': {'index': 0, 'rationale': "This demo shows what happens when a product team indicates they do not have the dedicated budget to support a distinct brand."}},
    "jvproduct": {'path': 'product', 'stage201': {'index': 1}, 'stage202': {'index': 1, 'rationale': "This demo shows the outcome for a product that belongs to a non-wholly-owned entity like a Joint Venture."}}
}


RESULT_DATA = {
    # Corporate Path Outcomes
    'basf_led': {'recommendation': "BASF-Led", 'rationale': "This entity's primary purpose is to be a direct expression of the BASF masterbrand and to build equity directly back to it. Its value is maximized by being an integral part of BASF.", 'activation_text': "This means we don't create a separate brand. The entity is branded simply as 'BASF [Entity Name]'. It lives on the main BASF website and is sold by the BASF sales team, reinforcing the power and innovation of the masterbrand.", 'examples': "Chemicals Division"},
    'endorsed_level1': {'recommendation': "BASF-Endorsed (Level 1: Co-Branded Lockup)", 'rationale': "This entity is a strategically critical pillar but requires its own distinct identity to win. The recommendation is a tight, explicit endorsement to transfer maximum trust from the masterbrand.", 'activation_text': "This triggers the **Co-Branded Lockup** playbook. The entity will have its own distinct brand identity but must use a mandatory visual co-branding system with the BASF logo. This provides the highest level of explicit backing and is reserved for our most important strategic ventures.", 'examples': "Chemovator GmbH"},
    'endorsed_level2': {'recommendation': "BASF-Endorsed (Level 2: Prominent Verbal Endorsement)", 'rationale': "This entity is an important, established brand that needs its own space but gains significant credibility and value from an explicit BASF link.", 'activation_text': "This triggers the **Prominent Verbal Endorsement** playbook. The brand operates with its own identity, supported by the classic 'powered by BASF' or 'A BASF Company' tagline. This provides a strong, clear connection that builds trust without a full visual lockup.", 'examples': "Coatings Division Brands"},
    'endorsed_level3': {'recommendation': "BASF-Endorsed (Level 3: Distant Verbal Endorsement)", 'rationale': "This entity is an exploratory venture that needs maximum independence. A subtle, distant link provides a 'halo' of quality while insulating the masterbrand from risk.", 'activation_text': "This triggers the **Distant Endorsement** playbook. The brand operates with full independence. The connection to BASF is strategic and not part of the primary brand identity. It is typically mentioned in non-consumer-facing contexts like 'About Us' sections, corporate reports, or investor relations.", 'examples': "NewBiz (Hypothetical)"},
    'flag_review': {'recommendation': "Flag for Strategic Review", 'rationale': "This entity's profile indicates a misalignment between its strategic importance and its market needs. This is a business issue, not a branding problem.", 'activation_text': "This is not a branding recommendation but a business flag. The combination of low strategic contribution and low market distinction need (or high need with low contribution) warrants a formal business review to determine the entity's future within the portfolio.", 'examples': "PolyWeld 800 Business"},
    # Product Path Outcomes
    'product_led': {'recommendation': "BASF-Led (Product Level)", 'rationale': "This product's value is maximized by leveraging the full trust and equity of the BASF masterbrand. There is no data-backed business case for the cost and complexity of a distinct identity.", 'activation_text': "The recommendation is to use the standard **'BASF Productname®'** lockup. This approach ensures market clarity, reinforces BASF's quality promise, and provides the strongest return on investment. Please consult the BASF Brand Portal for the correct templates and usage rules.", 'examples': "Ultramid®"},
    'product_endorsed': {'recommendation': "BASF-Endorsed (Product Level)", 'rationale': "This product is a cornerstone of a divisional strategy and has a proven, data-backed need for a distinct identity to win in its specific market.", 'activation_text': "This product has earned the right to a distinct brand identity. It must be supported by a mandatory, explicit endorsement (e.g., 'powered by BASF'). A full business case and brand plan must be submitted to the divisional leadership for approval before development.", 'examples': "Glasurit®"},
    'insufficient_resources': {'recommendation': "BASF-Led (Standard Lockup)", 'rationale': "Building and sustaining a distinct brand requires significant, long-term investment. Without dedicated resources, a new brand identity cannot succeed and may damage the BASF brand through inconsistent application.", 'activation_text': "The most effective way to build value for this product is to leverage the full strength and resources of the BASF masterbrand. The recommendation is to use the standard 'BASF Productname®' lockup. Please consult the BASF Brand Portal for the correct templates and usage rules.", 'examples': "Any product without a dedicated brand budget"},
    'evaluate_parent_entity': {'recommendation': "Evaluate Parent Entity First", 'rationale': "A product's branding cannot be decided until its parent company's relationship to BASF is defined.", 'activation_text': "This product belongs to an entity that is not wholly-owned by BASF (e.g., a Joint Venture). Please use the **Corporate Path** in this tool to evaluate the parent corporate entity first. The branding of its products must follow the guidelines and endorsement level established for the parent company.", 'examples': "Products from a Joint Venture"},
    # General Outcomes
    'legal_directive': {'recommendation': "Follow Legal Directive", 'rationale': "The branding for this entity is pre-determined by a binding legal or contractual agreement which must be followed.", 'activation_text': "The branding for this entity is dictated by a binding legal or contractual agreement. The primary action is to consult the specific legal documents (e.g., the Joint Venture agreement) and implement the branding exactly as specified.", 'examples': "BASF SONATRACH PropanChem"},
    'independent_risk': {'recommendation': "Independent (for risk insulation)", 'rationale': "The entity carries significant reputational risk and must be strategically independent and distanced from the masterbrand.", 'activation_text': "This means the entity must operate as a fully independent brand with no visible connection to BASF. This is a strategic decision to insulate the BASF masterbrand from any potential reputational risk associated with the entity.\n\n**Maintaining the BASF Connection:** While this entity operates independently, it must adhere to BASF's non-negotiable core principles, including Safety & Compliance Standards, Code of Conduct, and Legal Transparency of Ownership.", 'examples': "ExtractMax"},
    'retire_rebrand': {'recommendation': "Independent (Retire & Rebrand)", 'rationale': "The acquired brand's baggage is a liability. The recommendation is to make it independent by retiring the name and transitioning customers to a BASF brand.", 'activation_text': "This means the acquired brand identity will be retired. A formal plan must be created to migrate customers and assets to a new or existing BASF brand, thereby making the business independent of the problematic legacy name.\n\n**Maintaining the BASF Connection:** While this entity operates independently, it must adhere to BASF's non-negotiable core principles, including Safety & Compliance Standards, Code of Conduct, and Legal Transparency of Ownership.", 'examples': "OldChem Inc."}
}

# --- WEIGHTING SYSTEM ---
WEIGHTS = {
    'corporate_A': {'a1': 3, 'a2': 3, 'a3': 2, 'a4': 2, 'a5': 1},
    'corporate_B': {'b1': 3, 'b2': 3, 'b3': 2, 'b4': 2, 'b5': 1},
    'product_A': {'pa1': 3, 'pa2': 3, 'pa3': 2, 'pa4': 2, 'pa5': 1},
    'product_B': {'pb1': 3, 'pb2': 3, 'pb3': 2, 'pb4': 2, 'pb5': 1}
}
HIGH_THRESHOLD = 6

# --- INTERACTIVE IMAGE VIEWER FUNCTION ---
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

    def reset_app():
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
        if result['examples']:
            st.markdown(f"**Similar Examples:** *{result['examples']}*")
        st.markdown("---")
        if st.button("Evaluate Another Entity"): reset_app()
    
    st.title("🧭 The BASF Brand Compass")
    if st.session_state.stage == 0:
        # --- HOME PAGE ---
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
        
        corp_demos = {"Chemicals": "chemicals", "Chemovator": "chemovator", "NewBiz": "newbiz"}
        prod_demos = {"Glasurit": "glasurit", "Ultramid": "ultramid"}
        
        st.markdown("**Corporate Entity Demos**")
        cols = st.columns(3)
        for i, (name, key) in enumerate(corp_demos.items()):
            with cols[i % 3]:
                if st.button(name, key=key, use_container_width=True): start_evaluation(name, is_demo=True, demo_key=key)

        st.markdown("**Product Demos**")
        cols = st.columns(3)
        for i, (name, key) in enumerate(prod_demos.items()):
            with cols[i % 3]:
                if st.button(name, key=key, use_container_width=True): start_evaluation(name, is_demo=True, demo_key=key)

        st.markdown("---")
        st.subheader("Stress-Test Scenarios")
        stress_demos = {"PolyWeld 800 Business": "polyweld800business", "No-Resource Product": "noresourceproduct", "JV Product": "jvproduct"}
        cols = st.columns(3)
        for i, (name, key) in enumerate(stress_demos.items()):
            with cols[i]:
                if st.button(name, key=key, use_container_width=True): start_evaluation(name, is_demo=True, demo_key=key)

        with st.expander("View the Brand Compass Flowchart"):
            display_interactive_image("flowchart.png") 

    elif st.session_state.stage == 0.5:
        # --- STRATEGIC ROUTER ---
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        st.subheader("Qualification: Strategic Router")
        st.write("**What is the fundamental nature of the entity being evaluated?**")
        st.caption("This first step routes the entity to the correct evaluation path. Corporate entities have access to the full strategic spectrum, while products follow a more constrained and rigorous path.")
        
        path_options = ["A Corporate Entity (company, JV, business unit)", "A Product or Product Range"]
        
        # Pre-select based on demo path if available
        demo_path_index = 0 if st.session_state.path_type == 'corporate' else 1
        
        path_choice = st.radio("Select the entity type:", path_options, index=demo_path_index, key="path_router")
        
        if st.button("Proceed"):
            if path_choice == path_options[0]:
                st.session_state.path_type = 'corporate'
                set_stage(1)
            else:
                st.session_state.path_type = 'product'
                set_stage(201) # Start of Product Path
    
    else:
        # --- ALL OTHER STAGES ---
        if st.session_state.path_type == 'corporate':
            # --- CORPORATE PATH ---
            corp_stages = {
                1: {"header": "Audience & Value Gate", "question": "Who is the primary audience?", "options": ["External customers/partners", "Internal employees", "Temporary campaign/initiative"], "next": [2, 'internal_naming', 'comms_initiative']},
                2: {"header": "Mandatory Directives", "question": "Is branding dictated by a pre-existing legal or contractual requirement?", "options": ["No", "Yes"], "next": [3, 'legal_directive']},
                3: {"header": "Risk Profile", "question": "Does the entity carry significant reputational risk that could harm the masterbrand?", "options": ["No", "Yes"], "next": [4, 'independent_risk']},
                4: {"header": "Structural Sorter", "question": "What is its ownership structure?", "options": ["Wholly-owned BASF business", "Joint Venture", "Third-party partner", "Newly acquired company"], "next": [5, 4.1, 'follow_partner_guidelines', 4.2]},
                4.1: {"header": "Joint Venture Equity Check", "question": "What is BASF's equity share?", "options": ["Majority (≥50%)", "Minority (<50%)"], "next": [5, 'independent_minority']},
                4.2: {"header": "Acquisition Evaluation", "question": "Does the acquired brand have significant negative equity?", "options": ["No", "Yes"], "next": [5, 'retire_rebrand']}
            }
            if st.session_state.stage in corp_stages:
                config = corp_stages[st.session_state.stage]
                st.header(f"Evaluating: *{st.session_state.entity_name}* (Corporate Path)")
                st.subheader(config["header"])
                
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get(f"stage{st.session_state.stage}", {})
                rec_index = demo_data.get('index')
                
                choice = st.radio(config["question"], config["options"], index=rec_index)
                
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                
                if st.button("Proceed"):
                    next_stage = config["next"][config["options"].index(choice)]
                    if isinstance(next_stage, str): display_result(next_stage)
                    else: set_stage(next_stage)

            elif st.session_state.stage == 5:
                # --- CORPORATE SCORECARD ---
                st.header(f"Evaluating: *{st.session_state.entity_name}* (Corporate Path)")
                st.subheader("Phase 2: Classification - The Strategic Scorecard")
                
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage5', {})
                rec_A = demo_data.get('score_A_checks', {})
                rec_B = demo_data.get('score_B_checks', {})

                questions_A = {
                    'a1': 'Is it a cornerstone of the "Winning Ways" strategy?',
                    'a2': 'Does it directly deliver on a key corporate initiative?',
                    'a3': 'Is it a strategic pillar designed to win in a distinct market?',
                    'a4': 'Does it strongly support the corporate purpose?',
                    'a5': 'Does it operate within an established BASF core business segment?'
                }
                questions_B = {
                    'b1': 'Is there a known negative perception of the BASF brand for this specific audience?',
                    'b2': 'Does it compete primarily with focused "pure-players"?',
                    'b3': 'Does the business require a distinct, agile culture to succeed?',
                    'b4': 'Does this brand need to appeal directly to an end-consumer (B2C / B2B2C)?',
                    'b5': 'Does it need clear differentiation from other BASF offerings?'
                }

                score_A = 0
                score_B = 0

                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Part A: Strategic Contribution Score**")
                    checks_A = {}
                    for key, q_text in questions_A.items():
                        checks_A[key] = st.checkbox(q_text, value=rec_A.get(key, False), key=key)
                        if checks_A[key]: score_A += WEIGHTS['corporate_A'][key]
                    st.session_state.scores['A'] = score_A
                    st.write(f"**Score A: {score_A} / 11**")
                
                with col2:
                    st.info("**Part B: Market Distinction Score**")
                    checks_B = {}
                    for key, q_text in questions_B.items():
                        checks_B[key] = st.checkbox(q_text, value=rec_B.get(key, False), key=key)
                        if checks_B[key]: score_B += WEIGHTS['corporate_B'][key]
                    st.session_state.scores['B'] = score_B
                    st.write(f"**Score B: {score_B} / 11**")
                
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")
                
                if st.button("Calculate Recommendation"): set_stage(6)

            elif st.session_state.stage == 6:
                # --- CORPORATE RESULT LOGIC ---
                score_a_high = st.session_state.scores['A'] >= HIGH_THRESHOLD
                score_b_high = st.session_state.scores['B'] >= HIGH_THRESHOLD
                
                outcome_key = ''
                if score_a_high and not score_b_high: outcome_key = 'basf_led'
                elif score_a_high and score_b_high: outcome_key = 'endorsed_level1'
                elif not score_a_high and score_b_high: outcome_key = 'endorsed_level3'
                else: outcome_key = 'flag_review' # Low/Low
                
                # Placeholder for Level 2
                if 4 <= st.session_state.scores['A'] <= 5 and 4 <= st.session_state.scores['B'] <= 5:
                    outcome_key = 'endorsed_level2'

                display_result(outcome_key)

        elif st.session_state.path_type == 'product':
            # --- PRODUCT PATH ---
            if st.session_state.stage == 201:
                # --- RESOURCE VIABILITY GATE ---
                st.header(f"Evaluating: *{st.session_state.entity_name}* (Product Path)")
                st.subheader("Gate 1: Resource Viability")
                st.write("**Does this product/range have a dedicated and approved multi-year budget (3-5 years) and the necessary team resources to build and sustain a distinct brand identity (including marketing, communications, and design)?**")
                
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage201', {})
                rec_index = demo_data.get('index')
                
                choice = st.radio("Select an answer:", ["No", "Yes"], index=rec_index)
                
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")

                if st.button("Proceed"):
                    if choice == "No": display_result('insufficient_resources')
                    else: set_stage(202)

            elif st.session_state.stage == 202:
                 # --- LEGAL ENTITY CHECK ---
                st.header(f"Evaluating: *{st.session_state.entity_name}* (Product Path)")
                st.subheader("Gate 2: Ownership Check")
                st.write("**Is this product legally part of a wholly-owned BASF entity?**")

                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202', {})
                rec_index = demo_data.get('index')

                choice = st.radio("Select an answer:", ["Yes", "No (it belongs to a JV, etc.)"], index=rec_index)

                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")

                if st.button("Proceed"):
                    if choice == "No (it belongs to a JV, etc.)": display_result('evaluate_parent_entity')
                    else: set_stage(205)

            elif st.session_state.stage == 205:
                # --- PRODUCT SCORECARD ---
                st.header(f"Evaluating: *{st.session_state.entity_name}* (Product Path)")
                st.subheader("Phase 2: Classification - The High-Rigor Product Scorecard")

                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage205', {})
                rec_A = demo_data.get('score_A_checks', {})
                rec_B = demo_data.get('score_B_checks', {})
                rec_data = demo_data.get('data_mandate', "")

                questions_A = {
                    'pa1': 'Is this product a cornerstone of a major divisional strategy?',
                    'pa2': 'Does this product create a significant positive "halo effect" for the BASF masterbrand?',
                    'pa3': 'Does this product provide access to a new, strategically important customer segment?',
                    'pa4': 'Does this product have proven high revenue and/or margin potential?',
                    'pa5': 'Does this product represent a breakthrough technology or innovation?'
                }
                questions_B = {
                    'pb1': 'Does data prove it\'s needed to avoid portfolio confusion/cannibalization?',
                    'pb2': 'Does data prove it competes against consumer brands where \'BASF\' is a disadvantage?',
                    'pb3': 'Does data prove it competes against focused "pure-player" brands?',
                    'pb4': 'Does it require a unique, agile go-to-market approach?',
                    'pb5': 'Does data prove it needs differentiation from the BASF masterbrand to succeed?'
                }
                data_mandate_keys = ['pb1', 'pb2', 'pb3', 'pb5']

                score_A = 0
                score_B = 0
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Part A: Strategic Contribution Score**")
                    checks_A = {}
                    for key, q_text in questions_A.items():
                        checks_A[key] = st.checkbox(q_text, value=rec_A.get(key, False), key=key)
                        if checks_A[key]: score_A += WEIGHTS['product_A'][key]
                    st.session_state.scores['A'] = score_A
                    st.write(f"**Score A: {score_A} / 11**")

                with col2:
                    st.info("**Part B: Market Distinction Score**")
                    checks_B = {}
                    data_B = {}
                    for key, q_text in questions_B.items():
                        checks_B[key] = st.checkbox(q_text, value=rec_B.get(key, False), key=key)
                        if key in data_mandate_keys:
                            data_B[key] = st.text_area(f"Link to supporting data for Q: '{q_text}'", height=50, key=f"data_{key}", value=rec_data if key == 'pb1' else "")
                            if checks_B[key] and data_B[key].strip() != "":
                                score_B += WEIGHTS['product_B'][key]
                        elif checks_B[key]:
                            score_B += WEIGHTS['product_B'][key]
                    st.session_state.scores['B'] = score_B
                    st.write(f"**Score B: {score_B} / 11**")
                
                if demo_data.get('rationale'): st.info(f"**Demo Guidance:** {demo_data['rationale']}")

                if st.button("Calculate Recommendation"): set_stage(206)

            elif st.session_state.stage == 206:
                # --- PRODUCT RESULT LOGIC ---
                score_a_high = st.session_state.scores['A'] >= HIGH_THRESHOLD
                score_b_high = st.session_state.scores['B'] >= HIGH_THRESHOLD
                
                outcome_key = ''
                if score_a_high and score_b_high: outcome_key = 'product_endorsed'
                elif not score_a_high and score_b_high: outcome_key = 'flag_review'
                else: outcome_key = 'product_led' # Covers High/Low and Low/Low
                
                display_result(outcome_key)


# --- App Execution with Password Check ---
if check_password():
    run_app()
