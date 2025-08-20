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
    "chemicals": {'stage1': {'index': 0, 'rationale': "The Chemicals division sells products to external customers."}, 'stage2': {'index': 0, 'rationale': "There are no specific legal or contractual requirements..."}, 'stage3': {'index': 0, 'rationale': "This is the core business and carries a standard risk profile."}, 'stage4': {'index': 0, 'rationale': "The division is a wholly-owned and created part of BASF."}, 'stage5': {'rationale': "As the core of BASF's strategy, it scores high on contribution. As the masterbrand itself, it has no need for market distinction.", 'score_A_checks': [True, True, False, True, True], 'score_B_checks': [False, False, False, False, False]}},
    "agriculture": {'stage1': {'index': 0, 'rationale': "The Agriculture division sells products to external customers."}, 'stage2': {'index': 0, 'rationale': "Its branding is not dictated by a specific legal requirement."}, 'stage3': {'index': 0, 'rationale': "Its risks are standard for the industry."}, 'stage4': {'index': 0, 'rationale': "This is a wholly-owned BASF business."}, 'stage5': {'rationale': "As a key growth pillar competing with pure-players, it is strategically vital but needs its own brand to win.", 'score_A_checks': [False, True, True, True, False], 'score_B_checks': [True, True, False, True, False]}},
    "coatings": {'stage1': {'index': 0, 'rationale': "The Coatings division sells products to external customers."}, 'stage2': {'index': 0, 'rationale': "Its branding is not dictated by a specific legal requirement."}, 'stage3': {'index': 0, 'rationale': "Its risks are standard for the industry."}, 'stage4': {'index': 0, 'rationale': "This is a wholly-owned BASF business."}, 'stage5': {'rationale': "As a key growth pillar competing with pure-players, it is strategically vital but needs its own brand to win.", 'score_A_checks': [False, True, True, True, False], 'score_B_checks': [True, True, False, True, False]}},
    "ecms": {'stage1': {'index': 0, 'rationale': "ECMS sells products to external customers."}, 'stage2': {'index': 0, 'rationale': "Its branding is not dictated by a specific legal requirement."}, 'stage3': {'index': 0, 'rationale': "Its risks are standard for the industry."}, 'stage4': {'index': 0, 'rationale': "This is a wholly-owned BASF business."}, 'stage5': {'rationale': "As a sustainability-focused growth pillar, it's highly strategic but needs a distinct identity for its specialized market.", 'score_A_checks': [False, True, True, True, True], 'score_B_checks': [False, True, False, True, True]}},
    "xarvio": {'stage1': {'index': 0, 'rationale': "Xarvio is a commercial digital solution sold to farmers."}, 'stage2': {'index': 0, 'rationale': "There are no overriding legal requirements for this internally developed brand."}, 'stage3': {'index': 0, 'rationale': "As a digital product, it does not carry an above-average reputational risk."}, 'stage4': {'index': 0, 'rationale': "Xarvio was developed internally, making it a wholly-owned BASF brand."}, 'stage5': {'rationale': "Xarvio is a strategic growth driver needing its own brand to compete with agile tech players and overcome a 'big corporate' headwind.", 'score_A_checks': [False, False, True, True, True], 'score_B_checks': [True, True, True, True, True]}},
    "care360": {'stage1': {'index': 0, 'rationale': "This is a platform of solutions offered to external customers."}, 'stage2': {'index': 0, 'rationale': "There are no overriding legal requirements."}, 'stage3': {'index': 0, 'rationale': "Its risk profile is standard."}, 'stage4': {'index': 0, 'rationale': "It is a wholly-owned strategic initiative developed by BASF."}, 'stage5': {'rationale': "As a solutions platform, its entire purpose is to showcase the power of the masterbrand. It needs to be the embodiment of BASF, not distinct from it.", 'score_A_checks': [False, True, False, True, True], 'score_B_checks': [False, False, False, False, False]}},
    "newbiz": {'stage1': {'index': 0, 'rationale': "This is a commercial business that sells products externally."}, 'stage2': {'index': 0, 'rationale': "Its branding is not dictated by a specific legal requirement."}, 'stage3': {'index': 0, 'rationale': "Risk is standard for a new venture."}, 'stage4': {'index': 0, 'rationale': "This is a new, wholly-owned venture created by BASF."}, 'stage5': {'rationale': "This new venture is not yet core to strategy but needs high market distinction to succeed in a new field.", 'score_A_checks': [False, False, False, True, False], 'score_B_checks': [True, True, True, True, True]}},
    "newco": {'stage1': {'index': 0, 'rationale': "This is a commercial business that sells products externally."}, 'stage2': {'index': 0, 'rationale': "We assume the M&A deal has no unusual branding constraints."}, 'stage3': {'index': 0, 'rationale': "Assuming this is a standard acquisition, the risk profile is not above-average."}, 'stage4': {'index': 3, 'rationale': "As a 'newly acquired company,' its existing brand equity must be handled carefully."}, 'stage4.1': {'index': 0, 'rationale': "We are assuming 'NewCo' is a valuable asset with positive brand equity."}},
    "basfsonatrachpropanchem": {'stage1': {'index': 0, 'rationale': "This is a commercial business that sells products externally."}, 'stage2': {'index': 1, 'rationale': "As a Joint Venture, the branding is explicitly defined in the legal agreement that formed the company. This agreement must be followed."}},
    "insight360": {'stage1': {'index': 1, 'rationale': "This is a tool for internal employees, so it's not a public-facing brand."}},
    "anniversaries": {'stage1': {'index': 2, 'rationale': "This is a temporary campaign led by BASF, not a permanent brand in the portfolio."}},
    "polyweld800": {'stage1': {'index': 0, 'rationale': "This is a commercial product sold externally."}, 'stage2': {'index': 0, 'rationale': "There are no special legal requirements for this product."}, 'stage3': {'index': 0, 'rationale': "As a standard industrial adhesive, it carries no unusual reputational risk."}, 'stage4': {'index': 0, 'rationale': "It is a legacy, wholly-owned BASF product line."}, 'stage5': {'rationale': "This legacy product is no longer aligned with key strategies and does not need its own brand to compete on price, triggering a business review.", 'score_A_checks': [False, False, False, False, False], 'score_B_checks': [False, False, False, False, False]}},
    "extractmax": {'stage1': {'index': 0, 'rationale': "This is a commercial product sold externally."}, 'stage2': {'index': 0, 'rationale': "There are no special legal requirements for this product."}, 'stage3': {'index': 2, 'rationale': "Yes. Due to its use in a controversial industry, this product carries a significant reputational risk that could harm the masterbrand."}},
    "oldcheminc": {'stage1': {'index': 0, 'rationale': "This is a commercial business we have acquired."}, 'stage2': {'index': 0, 'rationale': "We assume the M&A deal has no unusual branding constraints."}, 'stage3': {'index': 0, 'rationale': "The business itself is not high-risk."}, 'stage4': {'index': 3, 'rationale': "This is a newly acquired company."}, 'stage4.1': {'index': 1, 'rationale': "Yes. The acquired brand has a known negative reputation that would be a liability for BASF to inherit."}}
}

RESULT_DATA = {
    'basf_led': {'recommendation': "BASF-Led", 'rationale': "The entity is a core expression of the BASF brand and benefits most from a direct connection.", 'activation_text': "This means we don't create a separate brand. The entity is branded simply as 'BASF [Entity Name]'. It lives on the main BASF website and is sold by the BASF sales team, reinforcing the power and innovation of the masterbrand.", 'examples': "Chemicals, Care 360°"},
    'basf_endorsed': {'recommendation': "BASF-Endorsed", 'rationale': "The entity is strategically vital but requires its own distinct brand to win in its specific market.", 'activation_text': "This means the entity has its own distinct brand and identity. The endorsement, such as 'powered by BASF science,' is used strategically to provide the ultimate reason to believe—giving the brand both the unique story it needs and the scientific credibility customers trust.", 'examples': "Agriculture, Coatings, Xarvio"},
    'basf_associated': {'recommendation': "BASF-Associated", 'rationale': "The entity is exploring a new space and needs brand independence. A lighter, strategic association provides credibility without high commitment.", 'activation_text': "This means the entity has its own independent brand. The connection to BASF is lighter and more strategic, often used in communications rather than on packaging. This provides credibility without tying the venture too closely to the masterbrand's core identity.", 'examples': "NewBiz"},
    'flag_review': {'recommendation': "Flag for Strategic Review", 'rationale': "The entity has a low strategic contribution and a low market distinction score.", 'activation_text': "This is not a branding recommendation but a business flag. It triggers a formal business review to determine the entity's future within the portfolio.", 'examples': "PolyWeld 800"},
    'internal_naming': {'recommendation': "Descriptor / Internal Naming", 'rationale': "This is an internal-facing tool, not a public brand. The Compass's work is complete.", 'activation_text': "This entity does not require a public-facing brand. It should be named and governed according to BASF's existing guidelines for internal logos. Please consult the 'Checklist for Brand Champions' and the 'Decision Tree for the use of internal logos' to proceed.", 'examples': "Insight 360"},
    'comms_initiative': {'recommendation': "Descriptor / Internal Naming", 'rationale': "This is a temporary communication initiative, not a permanent brand. The Compass's work is complete.", 'activation_text': "This entity does not require a public-facing brand. It should be named according to BASF's internal naming conventions for projects, tools, or initiatives.", 'examples': "Anniversaries"},
    'legal_directive': {'recommendation': "Follow Legal Directive", 'rationale': "The branding for this entity is pre-determined by a binding legal or contractual agreement which must be followed. The Compass's work is complete.", 'activation_text': "The branding for this entity is dictated by a binding legal or contractual agreement. The primary action is to consult the specific legal documents (e.g., the Joint Venture agreement) and implement the branding exactly as specified.", 'examples': "BASF SONATRACH PropanChem"},
    'independent_risk': {'recommendation': "Independent (for risk insulation)", 'rationale': "The entity carries significant reputational risk and must be strategically independent and distanced from the masterbrand.", 'activation_text': "This means the entity must operate as a fully independent brand with no visible connection to BASF. This is a strategic decision to insulate the BASF masterbrand from any potential reputational risk associated with the entity.\n\n**Maintaining the BASF Connection:** While this entity operates independently, it must adhere to BASF's non-negotiable core principles, including Safety & Compliance Standards, Code of Conduct, and Legal Transparency of Ownership.", 'examples': "ExtractMax"},
    'strategically_aligned': {'recommendation': "Strategically Aligned (Phased Approach)", 'rationale': "As a valuable acquisition or majority-owned JV with existing equity, the brand integration must be managed with a market-by-market plan to retain value. The Compass's work is complete.", 'activation_text': "This triggers a market-by-market integration plan. The brand's relationship to BASF will vary by region, from 'Maintain & Reassure' (e.g., 'Stoneville, from BASF') where its equity is high, to 'Lead with BASF' where its equity is low. The goal is to maximize value in every market.", 'examples': "NewCo"},
    'retire_rebrand': {'recommendation': "Independent (Retire & Rebrand)", 'rationale': "The acquired brand's baggage is a liability. The recommendation is to make it independent by retiring the name and transitioning customers to a BASF brand.", 'activation_text': "This means the acquired brand identity will be retired. A formal plan must be created to migrate customers and assets to a new or existing BASF brand, thereby making the business independent of the problematic legacy name.\n\n**Maintaining the BASF Connection:** While this entity operates independently, it must adhere to BASF's non-negotiable core principles, including Safety & Compliance Standards, Code of Conduct, and Legal Transparency of Ownership.", 'examples': "OldChem Inc."},
    'follow_partner_guidelines': {'recommendation': "Follow Partner/Distributor Guidelines", 'rationale': "Branding for third-party partners without a BASF equity stake is governed by specific legal and brand guidelines.", 'activation_text': "The primary action is to consult the official 'Distributor Branding Guidelines' and engage with the Brand Consultancy team to ensure full compliance before using any BASF branding. This ensures consistency and protects both brands.", 'examples': "Third-Party Distributors"},
    'independent_minority': {'recommendation': "Independent (Minority-owned JV)", 'rationale': "As a minority stakeholder, BASF cannot enforce its brand identity. The JV must operate with its own distinct brand to ensure legal and market clarity.", 'activation_text': "This entity requires its own independent brand identity. BASF's involvement should be communicated strategically as an endorsement or partnership, guided by the terms of the Joint Venture agreement, rather than through direct branding.", 'examples': "Minority-stake Joint Ventures"}
}

# --- INTERACTIVE IMAGE VIEWER FUNCTION (CORRECTED) ---
def display_interactive_image(image_path: str):
    """
    Creates a clickable thumbnail that opens a full-featured, interactive image viewer
    with zoom and pan capabilities, using the Viewer.js library.
    """
    # Read the image file and encode it in Base64
    try:
        image_bytes = Path(image_path).read_bytes()
        encoded_image = base64.b64encode(image_bytes).decode()
        image_html_src = f"data:image/png;base64,{encoded_image}"
    except FileNotFoundError:
        st.error(f"Image file not found at '{image_path}'. Make sure it's in the same directory as the script.")
        return

    # Self-contained HTML component with Viewer.js
    # NOTE: The 'integrity' and 'crossorigin' attributes have been removed to prevent blocking.
    html_code = f'''
    <!-- 1. Include the Viewer.js CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.3/viewer.min.css" />

    <!-- 2. The image that will be the trigger -->
    <div id="image-container">
      <img id="flowchart-image" src="{image_html_src}" alt="Brand Compass Flowchart" style="max-width: 100%; cursor: zoom-in;">
    </div>
    <p style="text-align:center; color:grey;">Click image to open interactive viewer</p>

    <!-- 3. Include the Viewer.js JavaScript -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.3/viewer.min.js"></script>
    
    <!-- 4. Initialize Viewer.js -->
    <script>
      const viewer = new Viewer(document.getElementById('flowchart-image'), {{
        inline: false, // Don't show the viewer directly
        toolbar: {{
            zoomIn: 1,
            zoomOut: 1,
            oneToOne: 1,
            reset: 1,
            prev: 0, 
            play: {{ show: 0 }},
            next: 0, 
            rotateLeft: 1,
            rotateRight: 1,
            flipHorizontal: 1,
            flipVertical: 1,
        }},
      }});
    </script>
    '''
    st.components.v1.html(html_code, height=400)


# --- Main App Function ---
def run_app():
    if 'stage' not in st.session_state: st.session_state.stage = 0
    if 'entity_name' not in st.session_state: st.session_state.entity_name = ""
    if 'scores' not in st.session_state: st.session_state.scores = {'A': 0, 'B': 0}
    if 'demo_key' not in st.session_state: st.session_state.demo_key = None

    def start_evaluation(entity_name):
        st.session_state.entity_name = entity_name
        demo_key_check = entity_name.lower().strip().replace('°', '').replace(' ', '')
        if demo_key_check in DEMO_DATA: st.session_state.demo_key = demo_key_check
        set_stage(1)

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
        
        standard_demos = ["Chemicals", "Xarvio", "NewBiz", "BASF Sonatrach PropanChem", "NewCo", "Anniversaries", "Coatings", "ECMS", "Care 360°", "Insight 360", "Agriculture"]
        cols = st.columns(4)
        for i, brand_key in enumerate(standard_demos):
            with cols[i % 4]:
                if st.button(brand_key, key=brand_key.lower().replace(' ', ''), use_container_width=True): start_evaluation(brand_key)

        st.markdown("---")
        st.subheader("Stress-Test Scenarios")
        stress_demos = ["PolyWeld 800", "ExtractMax", "OldChem Inc."]
        cols = st.columns(3)
        for i, brand_key in enumerate(stress_demos):
            with cols[i]:
                if st.button(brand_key, key=brand_key.lower().replace(' ', ''), use_container_width=True): start_evaluation(brand_key)

        with st.expander("View the Brand Compass Flowchart"):
            display_interactive_image("flowchart.png") 
    
    else:
        stage_config = {
            1: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Audience & Value Gate", "explanation": "This first step determines if the entity is a commercial brand requiring a strategic decision based on its audience.", "question": "Who is the primary audience, and what is its core value proposition?", "options": ["External customers/partners (product, service, or solution)", "Internal employees (tool, platform, or resource)", "External stakeholders (temporary campaign or initiative)"], "next_stages": [2, 101, 102]},
            2: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Mandatory Directives", "explanation": "This step checks for any non-negotiable legal or contractual obligations that pre-determine the branding approach.", "question": "Is branding dictated by a pre-existing legal or contractual requirement?", "options": ["No", "Yes"], "next_stages": [3, 103]},
            3: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Risk & Opportunity Profile", "explanation": "This is a safety check to determine if the entity carries a significant reputational risk that could harm the masterbrand, or a unique opportunity to enhance it.", "question": "What is the reputational risk/opportunity profile?", "options": ["Standard Profile: Risk is manageable and aligned with BASF's core business.", "High Opportunity: Carries unique potential to enhance BASF's reputation in a new/strategic area.", "High Risk: Carries significant reputational risk that could negatively impact the masterbrand."], "next_stages": [4, 4, 104]},
            4: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Structural Sorter", "explanation": "This step sorts entities based on their ownership, as special cases like JVs, Partners, and Acquisitions have unique strategic needs.", "question": "What is its ownership structure?", "options": ["A wholly-owned BASF business", "A Joint Venture (where BASF has an equity stake)", "A third-party partner or distributor (with no BASF equity)", "A newly acquired company"], "next_stages": [5, 4.2, 108, 4.1]},
            4.1: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Acquisition Evaluation", "explanation": "For acquired brands, we must assess their existing reputation to decide whether to leverage their brand equity or retire it.", "question": "Does the acquired brand have significant negative equity?", "options": ["No", "Yes"], "next_stages": [106, 107]},
            4.2: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Joint Venture Agreement Check", "explanation": "Some Joint Venture agreements contain specific branding clauses that must be followed.", "question": "Are there pre-existing brand guidelines in the JV/Alliance agreement?", "options": ["No, branding is flexible", "Yes, branding is defined in the agreement"], "next_stages": [4.3, 103]},
            4.3: {"phase_name": "Phase 1: Qualification - The 'What'", "header": "Joint Venture Equity Check", "explanation": "BASF's equity stake is a key factor in determining the appropriate branding approach for a Joint Venture.", "question": "What is BASF's equity share in the Joint Venture?", "options": ["Majority (≥50%)", "Minority (<50%)"], "next_stages": [106, 109]}
        }

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
            
            s_choice = st.radio(current_config["question"], format_options(current_config["options"], recommended_index), index=recommended_index, key=f"s{st.session_state.stage}_radio")
            
            if recommended_index is not None: st.info(f"**Demo Guidance:** {demo_path_data[stage_key]['rationale']}")

            # --- CIRCUIT BREAKER ---
            st.markdown("---")
            data_provided = st.checkbox("I have provided the necessary data to make an informed decision at this stage.")
            st.text_area("Link to supporting documents (e.g., business case, project charter, communications brief)", key=f"data_link_{st.session_state.stage}", height=100)
            st.markdown("---")
            
            if st.button("Proceed", type="primary", disabled=not data_provided):
                selected_index = current_config["options"].index(s_choice.strip('*'))
                set_stage(current_config["next_stages"][selected_index])
            elif not data_provided:
                st.warning("Please confirm you have linked to supporting data before proceeding.")


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
                a1 = st.checkbox('Does it operate within an established BASF core business segment?', value=rec_checks_A[0])
                a2 = st.checkbox('Is it a cornerstone brand for the "Winning Ways" strategy?', value=rec_checks_A[1])
                a3 = st.checkbox('Is it a strategic pillar designed to win in a distinct market or business model?', value=rec_checks_A[2])
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
        
        else: # This block handles ALL final recommendation pages
            result_key_map = {
                101: 'internal_naming', 102: 'comms_initiative', 103: 'legal_directive',
                104: 'independent_risk', 105: 'strategically_aligned', 106: 'strategically_aligned',
                107: 'retire_rebrand', 108: 'follow_partner_guidelines', 109: 'independent_minority'
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
                display_result(outcome_key)

# --- App Execution with Password Check ---
if check_password():
    run_app()
