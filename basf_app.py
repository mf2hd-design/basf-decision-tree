import streamlit as st
import base64
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="BASF Brand Compass",
    page_icon="🧭",
    layout="wide"  # FIX 10: wide layout gives scorecard columns room to breathe
)

# --- Password Protection Logic ---
def check_password():
    """Returns `True` if the user is logged in."""
    if st.session_state.get("password_correct", False):
        return True

    st.title("🧭 The BASF Brand Compass")
    with st.form("password_form"):
        password_input = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Submit")

    if submitted:
        if password_input == "2025FFxBASFxFF":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("😕 Password incorrect")

    return False

# --- Data Libraries ---
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
    # Corporate Path Outcomes
    'basf_led': {
        'recommendation': "BASF Branded",
        'rationale': "This entity's primary purpose is to be a direct expression of the BASF masterbrand. Its value is maximized by being an integral part of BASF.",
        'activation_text': "This means we don't create a separate brand. The entity is branded simply as 'BASF [Entity Name]'. It lives on the main BASF website and is sold by the BASF sales team, reinforcing the power and innovation of the masterbrand.",
        'examples': "Chemicals Division, Internal Tools"
    },
    'endorsed_level1': {
        'recommendation': "BASF-Endorsed (Level 1: Co-Branded Lockup)",
        'rationale': "This entity is a strategically critical pillar but requires its own distinct identity to win. The recommendation is a tight, explicit endorsement.",
        'activation_text': "This triggers the **Co-Branded Lockup** playbook. The entity will have its own distinct brand identity but must use a mandatory visual co-branding system with the BASF logo.",
        'examples': "Chemovator GmbH"
    },
    'endorsed_level2': {
        'recommendation': "BASF-Endorsed (Level 2: Prominent Verbal Endorsement)",
        'rationale': "This entity is an important, established brand that needs its own space but gains significant credibility from an explicit BASF link.",
        'activation_text': "This triggers the **Prominent Verbal Endorsement** playbook. The brand operates with its own identity, supported by the classic 'powered by BASF' or 'A BASF Company' tagline.",
        'examples': "Coatings Division Brands"
    },
    'endorsed_level3': {
        'recommendation': "BASF-Endorsed (Level 3: Distant Verbal Endorsement)",
        'rationale': "This entity is an exploratory venture that needs maximum independence. A subtle, distant link provides a 'halo' of quality while insulating the masterbrand from risk.",
        'activation_text': "This triggers the **Distant Endorsement** playbook. The brand operates with full independence. The connection to BASF is strategic and not part of the primary brand identity.",
        'examples': "NewBiz (Hypothetical), Metivo"
    },
    'flag_review': {
        'recommendation': "Flag for Strategic Review",
        'rationale': "This entity's profile indicates a misalignment. This could be due to low strategic importance, a lack of resources, or other factors. This is a business issue, not just a branding problem.",
        'activation_text': "This is not a branding recommendation but a business flag. The entity's situation warrants a formal business review to determine its future within the portfolio.",
        'examples': "PolyWeld 800 Business"
    },

    # FIX 1: Correct outcome for non-commercial entities
    'non_commercial': {
        'recommendation': "Use Existing Brand & Identity",
        'rationale': "Non-commercial entities — including campaigns, events, trade fairs, and internal initiatives — do not require their own brand. They should use the existing brand and visual identity of the entity they belong to.",
        'activation_text': "Apply the visual identity of the parent entity consistently across all communications for this initiative.\n\nA standalone logo may only be considered if the initiative meets specific criteria around duration, audience size, and touchpoint frequency. Consult your Brand Champion if you believe those criteria are met.",
        'examples': "Marketing campaigns, trade fair presences, internal R&D projects, anniversary events"
    },

    # Product Path Outcomes
    'product_led': {
        'recommendation': "BASF Branded (Product Level)",
        'rationale': "This product's value is maximized by leveraging the full trust and equity of the BASF masterbrand. There is no data-backed business case for a distinct identity.",
        'activation_text': "The recommendation is to use the standard **'BASF Productname®'** lockup. This approach ensures market clarity, reinforces BASF's quality promise, and provides the strongest return on investment.",
        'examples': "Ultramid®"
    },
    'product_endorsed': {
        'recommendation': "BASF-Endorsed (Product Level)",
        'rationale': "This product is a cornerstone of a divisional strategy and has a proven, data-backed need for a distinct identity to win.",
        'activation_text': "This product has earned the right to a distinct brand identity. It must be supported by a mandatory, explicit endorsement (e.g., 'powered by BASF').",
        'examples': "Glasurit®"
    },
    'insufficient_resources': {
        'recommendation': "Flag for Review (Insufficient Resources)",
        'rationale': "Building and sustaining a distinct brand requires significant, long-term investment. Without dedicated resources, a new brand identity cannot succeed.",
        'activation_text': "The entity does not have the required resources to support a distinct brand. This triggers a **Flag for Review**.",
        'examples': "Any product without a dedicated brand budget"
    },
    'evaluate_parent_entity': {
        'recommendation': "Evaluate Parent Entity First",
        'rationale': "A product's branding cannot be decided until its parent company's relationship to BASF is defined.",
        'activation_text': "This product belongs to an entity that is not wholly-owned by BASF (e.g., a Joint Venture). Please use the **Corporate Path** to evaluate the parent corporate entity first.",
        'examples': "Products from a Joint Venture"
    },

    # General Outcomes
    'not_governed_by_basf': {
        'recommendation': "Not Governed by BASF Brand",
        'rationale': "The entity is deployed and managed by an independent business that does not currently use the BASF brand.",
        'activation_text': "This entity falls outside the governance of the BASF brand architecture. The recommendation is to treat it as 'Independent'.",
        'examples': "Wintershall Dea subsidiary"
    },
    'legal_directive': {
        'recommendation': "Follow Legal Directive",
        'rationale': "A binding legal or contractual agreement decides the branding for this entity.",
        'activation_text': "The primary action is to consult the specific legal documents (e.g., the Joint Venture agreement) and implement the branding exactly as specified.",
        'examples': "BASF SONATRACH PropanChem"
    },
    'independent_risk': {
        'recommendation': "Independent (Risk Insulation)",
        'rationale': "The entity has the potential to create significant negative reputation impact or channel conflict.",
        'activation_text': "This means the entity must operate as a fully independent brand with no visible connection to BASF. This is a strategic decision to create a 'reputational firewall'.",
        'examples': "ExtractMax"
    },
    'follow_partner_guidelines': {
        'recommendation': "Follow Partner/Distributor Guidelines",
        'rationale': "As a third-party partner/distributor with no BASF equity stake, branding is governed by specific legal and brand guidelines.",
        'activation_text': "The primary action is to consult the official 'Distributor Branding Guidelines'.",
        'examples': "Third-Party Distributors"
    },
    'independent_minority': {
        'recommendation': "Independent (Minority-owned JV)",
        'rationale': "As a minority stakeholder (<50% equity), BASF cannot enforce its brand identity.",
        'activation_text': "This entity requires its own independent brand identity. BASF's involvement should be communicated strategically as an endorsement or partnership.",
        'examples': "Minority-stake Joint Ventures"
    },
    'retire_rebrand': {
        'recommendation': "Independent (Retire & Rebrand)",
        'rationale': "The acquired brand has negative equity/reputation, making its association a liability.",
        'activation_text': "This means the acquired brand identity will be retired. A formal plan must be created to migrate customers and assets to a new or existing BASF brand.",
        'examples': "OldChem Inc."
    }
}

WEIGHTS = {
    'corporate_A': {'a1': 3, 'a2': 3, 'a3': 2, 'a4': 2, 'a5': 1},
    'corporate_B': {'b1': 3, 'b2': 3, 'b3': 2, 'b4': 2, 'b5': 1},
    'product_A': {'pa1': 3, 'pa2': 3, 'pa3': 2, 'pa4': 2, 'pa5': 1},
    'product_B': {'pb1': 3, 'pb2': 3, 'pb3': 2, 'pb4': 2, 'pb5': 1}
}
HIGH_THRESHOLD = 6

# FIX 5: progress maps — stage → (current step, total steps, label)
CORPORATE_PROGRESS = {
    1: (1, 5, "Fast Track 1: Ownership"),
    1.1: (1, 5, "Fast Track 1: Ownership"),
    1.2: (1, 5, "Fast Track 1: Ownership"),
    1.3: (1, 5, "Fast Track 1: Ownership"),
    2: (2, 5, "Fast Track 2: Risk Profile"),
    3: (3, 5, "Fast Track 3: Legal Directives"),
    4: (4, 5, "Fast Track 4: Resources"),
    5: (5, 5, "Scorecard"),
}
PRODUCT_PROGRESS = {
    201: (1, 6, "Fast Track 1: Governance"),
    202: (2, 6, "Fast Track 2: Ownership"),
    202.1: (2, 6, "Fast Track 2: Ownership"),
    202.2: (2, 6, "Fast Track 2: Ownership"),
    202.3: (2, 6, "Fast Track 2: Ownership"),
    203: (3, 6, "Fast Track 3: Risk Profile"),
    204: (4, 6, "Fast Track 4: Legal Directives"),
    205: (5, 6, "Fast Track 5: Resources"),
    206: (6, 6, "Scorecard"),
}


# --- Main App Function ---
def run_app():
    # Initialise session state
    if 'stage' not in st.session_state: st.session_state.stage = 0
    if 'entity_name' not in st.session_state: st.session_state.entity_name = ""
    if 'scores' not in st.session_state: st.session_state.scores = {'A': 0, 'B': 0}
    if 'demo_key' not in st.session_state: st.session_state.demo_key = None
    if 'path_type' not in st.session_state: st.session_state.path_type = None
    if 'stage_history' not in st.session_state: st.session_state.stage_history = []  # FIX 4

    def start_evaluation(entity_name, is_demo=False, demo_key=None):
        st.session_state.entity_name = entity_name
        st.session_state.stage_history = []
        if is_demo and demo_key:
            st.session_state.demo_key = demo_key
            st.session_state.path_type = DEMO_DATA[demo_key].get('path', 'corporate')
        set_stage(0.5)

    def set_stage(stage_num):
        # FIX 4: push current stage onto history stack before advancing
        st.session_state.stage_history.append(st.session_state.stage)
        st.session_state.stage = stage_num
        st.rerun()

    def go_back():
        if st.session_state.stage_history:
            st.session_state.stage = st.session_state.stage_history.pop()
            st.rerun()

    def reset_app_callback():
        keys_to_delete = [key for key in st.session_state.keys() if key != 'password_correct']
        for key in keys_to_delete:
            del st.session_state[key]
        st.session_state.stage = 0

    def show_nav(stage):
        """Render back button and progress indicator for a given stage."""
        col_back, col_progress = st.columns([1, 6])
        with col_back:
            # FIX 4: back button — only shown when there is history to return to
            if st.session_state.stage_history:
                st.button("← Back", on_click=go_back, key=f"back_{stage}")
        with col_progress:
            # FIX 5: progress indicator
            progress_map = None
            if st.session_state.path_type == 'corporate':
                progress_map = CORPORATE_PROGRESS
            elif st.session_state.path_type == 'product':
                progress_map = PRODUCT_PROGRESS
            if progress_map and stage in progress_map:
                step, total, label = progress_map[stage]
                st.caption(f"Step {step} of {total} — {label}")

    def display_result(result_key):
        result = RESULT_DATA.get(result_key, {
            'recommendation': 'Error', 'rationale': 'Result key not found.',
            'activation_text': '', 'examples': ''
        })

        # FIX 4: back button on result screen
        if st.session_state.stage_history:
            st.button("← Back", on_click=go_back, key="back_result")

        st.header("Result")
        st.write(f"**Entity Evaluated:** *{st.session_state.entity_name}*")

        # FIX 2: show the scores that drove the recommendation
        score_a = st.session_state.scores.get('A', 0)
        score_b = st.session_state.scores.get('B', 0)
        if score_a > 0 or score_b > 0:
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Strategic Contribution (A)", f"{score_a} / 11",
                          help="Measures this entity's strategic importance to BASF.")
            with c2:
                st.metric("Market Distinction (B)", f"{score_b} / 11",
                          help="Measures how much this entity needs its own brand identity to succeed.")

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

    # ------------------------------------------------------------------ #
    st.title("🧭 The BASF Brand Compass")

    # ================================================================== #
    # STAGE 0 — HOME
    # ================================================================== #
    if st.session_state.stage == 0:
        st.markdown("An interactive tool to provide clear, strategic direction for the BASF brand architecture.")
        st.subheader("Evaluate a New Entity")

        # FIX 6: placeholder text on entity name input
        entity_name_input = st.text_input(
            "Enter name:", key="entity_name_input",
            label_visibility="collapsed",
            placeholder="e.g. Chemovator GmbH"
        )
        # FIX 9: cleaner button label
        if st.button("Begin Evaluation"):
            if entity_name_input:
                start_evaluation(entity_name_input)
            else:
                st.warning("Please enter an entity name to begin.")

        st.markdown("---")

        # FIX 7: captions added to standard and product demos
        st.subheader("Or, start a guided demo for a known brand:")
        st.markdown("**Standard Demos (Corporate-Level)**")
        standard_demos = {
            "Chemicals":                    "BASF's core masterbrand business unit",
            "Chemovator":                   "BASF's innovation and venture arm",
            "NewBiz":                       "Hypothetical exploratory venture",
            "BASF Sonatrach PropanChem":    "JV with a binding legal brand directive",
            "NewCo":                        "Recently acquired company with positive equity",
            "Anniversaries":               "Non-commercial campaign",
            "Coatings":                    "Growth division competing with pure-players",
            "ECMS":                        "Sustainability-focused growth pillar",
            "Care 360°":                   "Solutions platform closely tied to BASF",
            "Insight 360":                 "Internal tool",
        }
        cols = st.columns(5)
        for i, (brand_name, caption) in enumerate(standard_demos.items()):
            with cols[i % 5]:
                demo_key = brand_name.lower().replace(' ', '').replace('°', '')
                if st.button(brand_name, key=demo_key, use_container_width=True):
                    start_evaluation(brand_name, is_demo=True, demo_key=demo_key)
                st.caption(caption)

        st.markdown("**Product-Level Demos**")
        product_demos = {
            "Glasurit": "Cornerstone refinish brand, Coatings division",
            "Ultramid": "Workhorse B2B ingredient brand",
        }
        cols = st.columns(5)
        for i, (brand_name, caption) in enumerate(product_demos.items()):
            with cols[i % 5]:
                demo_key = brand_name.lower()
                if st.button(brand_name, key=demo_key, use_container_width=True):
                    start_evaluation(brand_name, is_demo=True, demo_key=demo_key)
                st.caption(caption)

        st.markdown("---")
        st.subheader("Stress-Test Scenarios")
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

        with st.expander("Download the Brand Compass Decision Tree PDF"):
            try:
                with open("document.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button(
                    label="Download PDF",
                    data=PDFbyte,
                    file_name="BASF_Decision_Tree.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except FileNotFoundError:
                st.error("File not found: 'document.pdf'.")

    # ================================================================== #
    # STAGE 0.5 — STRATEGIC ROUTER: Commercial vs Non-commercial
    # ================================================================== #
    elif st.session_state.stage == 0.5:
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        if st.session_state.stage_history:
            st.button("← Back", on_click=go_back, key="back_0.5")
        st.subheader("Strategic Router")
        st.markdown("""
**What is the purpose of the entity being evaluated?**

- **Commercial:** The entity is market-facing and has its own Profit & Loss (P&L).
  *Examples: A business unit, a subsidiary company, a product line.*

- **Non-commercial:** Any other activity, even if it supports commercial goals.
  *Examples: Marketing campaigns, events, trade fairs, internal initiatives, R&D projects.*
        """)

        path_options = ["Commercial", "Non-commercial"]
        demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage0.5', {})
        rec_index = demo_data.get('index')

        path_choice = st.radio("Select the entity's purpose:", path_options, index=rec_index, key="purpose_router")
        if demo_data.get('rationale'):
            st.info(f"**Demo Guidance:** {demo_data['rationale']}")

        if st.button("Proceed"):
            if path_choice == path_options[1]:
                # FIX 1: correct result for non-commercial entities
                display_result('non_commercial')
            else:
                set_stage(0.6)

    # ================================================================== #
    # STAGE 0.6 — ENTITY TYPE ROUTER: Corporate vs Product
    # ================================================================== #
    elif st.session_state.stage == 0.6:
        st.header(f"Evaluating: *{st.session_state.entity_name}*")
        if st.session_state.stage_history:
            st.button("← Back", on_click=go_back, key="back_0.6")
        st.subheader("Strategic Router")
        st.write("**What is the nature of the entity?**")

        path_options = ["Corporate Entity (e.g., a company, JV, business unit)", "Product, Service, or Solution"]
        demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage0.6', {})
        rec_index = demo_data.get('index')

        path_choice = st.radio("Select the entity type:", path_options, index=rec_index,
                               key="path_router", label_visibility="collapsed")

        if st.button("Proceed"):
            if path_choice == path_options[0]:
                st.session_state.path_type = 'corporate'
                set_stage(1)
            else:
                st.session_state.path_type = 'product'
                set_stage(201)

    else:
        # ============================================================== #
        # CORPORATE PATH
        # ============================================================== #
        if st.session_state.path_type == 'corporate':
            st.header(f"Evaluating: *{st.session_state.entity_name}* (Corporate Path)")

            if st.session_state.stage == 1:
                show_nav(1)
                st.write("**What is the ownership structure?**")
                options = ["Partner / Distributor", "Wholly Owned", "Joint Venture"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1', {})
                choice = st.radio("Select ownership structure:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == options[0]: display_result('follow_partner_guidelines')
                    elif choice == options[1]: set_stage(1.1)
                    else: set_stage(1.3)

            elif st.session_state.stage == 1.1:
                show_nav(1.1)
                st.write("**Is it an acquisition?**")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.1', {})
                choice = st.radio("Select if it is an acquisition:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": set_stage(1.2)
                    else: set_stage(2)

            elif st.session_state.stage == 1.2:
                show_nav(1.2)
                st.write("**Does the acquired brand have Negative Brand Equity?**")
                st.caption("E.g., known bad reputation, scandal, or safety failures.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.2', {})
                choice = st.radio("Select if it has negative equity:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('retire_rebrand')
                    else: set_stage(2)

            elif st.session_state.stage == 1.3:
                show_nav(1.3)
                st.write("**What is BASF's ownership share in the Joint Venture?**")
                options = ["Majority (50% or more)", "Minority (less than 50%)"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage1.3', {})
                choice = st.radio("Select ownership share:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == options[1]: display_result('independent_minority')
                    else: set_stage(2)

            elif st.session_state.stage == 2:
                show_nav(2)
                st.write("**Could it harm BASF's reputation?**")
                st.caption("Examples: Controversial industry, channel conflict with key customers, or high-risk technology.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage2', {})
                choice = st.radio("Select if there is a potential for negative impact:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('independent_risk')
                    else: set_stage(3)

            elif st.session_state.stage == 3:
                show_nav(3)
                st.write("**Does a legal contract already decide the brand?**")
                st.caption("E.g., Joint Venture agreement or licensing deal.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage3', {})
                choice = st.radio("Select if a contract decides the brand:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('legal_directive')
                    else: set_stage(4)

            elif st.session_state.stage == 4:
                show_nav(4)
                st.write("**Does it have dedicated Brand Management resources?**")
                st.caption("This means budget/team for design, research, and long-term brand building — not just product marketing.")
                options = ["No", "Yes"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage4', {})
                choice = st.radio("Select if resources are dedicated:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "No": display_result('flag_review')
                    else: set_stage(5)

            elif st.session_state.stage == 5:
                show_nav(5)
                st.caption("The entity has passed all Fast Tracks. Score its strategic value and its need for a distinct brand.")
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage5', {})
                rec_A = demo_data.get('score_A_checks', {})
                rec_B = demo_data.get('score_B_checks', {})

                questions_A = {
                    'a1': "A) Business Strategy: Is this entity linked to a top priority of BASF's business strategy?",
                    'a2': "B) Key Initiative: Does this entity help achieve a major company goal or performance target (KPI)?",
                    'a3': "C) Future Value: Does this entity help us win in a new market, segment, or business model?",
                    'a4': "D) Brand Character: Does this entity strongly support or demonstrate our desired brand positioning?",
                    'a5': "E) Operational Synergy: Does this entity's business model rely on deep operational integration with BASF's core capabilities?"
                }
                questions_B = {
                    'b1': "A) Reputation: Is there a known negative perception of the BASF brand among this entity's audience or in the market it operates?",
                    'b2': "B) Category: Does this entity operate in markets with norms or expectations that may not align with BASF's conventional practices?",
                    'b3': "C) Competitors: Does this entity compete primarily against specialised players?",
                    'b4': "D) Customers: Does this entity need to sell directly to end-customers using specific consumer marketing?",
                    'b5': "E) Ways of Working: Does this entity have a distinct way of working, compared to BASF, that forms part of its unique value proposition?"
                }

                # FIX 8: example text in collapsible expanders to reduce visual density
                examples_A = {
                    'a1': "E.g. It enhances our footprint in high-growth markets. It reinforces our leading cost position in key value chains. It improves reliability and product quality. It provides greater strategic and operational flexibility. It increases our ability to supply local markets. It enables our green transformation.",
                    'a2': "E.g. It helps harness AI-driven productivity and innovation. It drives net-zero measures.",
                    'a3': "E.g. It provides access to a previously untapped region or a new customer segment. It helps us target markets further along the supply chain. It allows us to form new strategic partnerships. It allows us to compete in an innovative, high-potential field.",
                    # FIX 3: clearly flag the placeholder before it goes in front of a client
                    'a4': "⚠️ Examples to be confirmed with the BASF team based on final brand positioning — do not use in client sessions until updated.",
                    'a5': "E.g. It relies on BASF's expertise or R&D capabilities. It leverages proprietary data, formulations or patents. It uses BASF's testing and certification systems. It depends on access to BASF's production infrastructure. It uses BASF's sourcing or distribution networks, technology systems or human resources. It leverages BASF's strategic partnerships."
                }
                examples_B = {
                    'b1': "E.g. For this audience/in this market BASF is perceived as 'slow-moving', 'operationally complex', having a large 'environmental footprint', 'exposed to market risk', too 'chemically focused', 'excessively diversified', etc.",
                    'b2': "E.g. Markets that are highly regulated, digital-first, fast-moving or experimental, sustainability-focused. Markets where clients expect hyper-tailored solutions, co-creation, extreme price-flexibility, modular product offerings, outcome-based commercial models, etc.",
                    'b3': "E.g. Competitors are narrowly focused on one specific area. They have category-specific value propositions and include category codes in their identity. They target narrowly defined audience segments through tailored messaging, category-specific channels and using a dedicated brand.",
                    'b4': "E.g. It bypasses intermediaries and sells its offer directly to final buyers or through distributors. It relies on consumer-focused channels and messaging in order to reach and appeal to its audience.",
                    'b5': "E.g. Uses rapid prototyping and iterative testing, offers highly tailored solutions, employs niche specialists. Has a flat hierarchy or cross-functional teams. Its operations are localised or decentralised. Offers a highly attentive, personalised approach to customer service."
                }

                score_A, score_B = 0, 0
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Part A: Strategic Contribution**")
                    for key, q_text in questions_A.items():
                        if st.checkbox(q_text, value=rec_A.get(key, False), key=key):
                            score_A += WEIGHTS['corporate_A'][key]
                        with st.expander("See examples"):
                            st.caption(examples_A[key])
                    st.session_state.scores['A'] = score_A
                    st.write(f"**Score A: {score_A} / 11**")
                with col2:
                    st.info("**Part B: Market Distinction**")
                    for key, q_text in questions_B.items():
                        if st.checkbox(q_text, value=rec_B.get(key, False), key=key):
                            score_B += WEIGHTS['corporate_B'][key]
                        with st.expander("See examples"):
                            st.caption(examples_B[key])
                    st.session_state.scores['B'] = score_B
                    st.write(f"**Score B: {score_B} / 11**")

                if st.button("Calculate Recommendation"):
                    set_stage(6)

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

        # ============================================================== #
        # PRODUCT PATH
        # ============================================================== #
        elif st.session_state.path_type == 'product':
            st.header(f"Evaluating: *{st.session_state.entity_name}* (Product Path)")

            if st.session_state.stage == 201:
                show_nav(201)
                st.write("**Is it managed by an independent business outside the BASF brand?**")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage201', {})
                choice = st.radio("Select an answer:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('not_governed_by_basf')
                    else: set_stage(202)

            elif st.session_state.stage == 202:
                show_nav(202)
                st.write("**What is the ownership structure?**")
                options = ["Partner / Distributor", "Wholly Owned", "Joint Venture"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202', {})
                choice = st.radio("Select ownership structure:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == options[0]: display_result('follow_partner_guidelines')
                    elif choice == options[1]: set_stage(202.1)
                    else: set_stage(202.2)

            elif st.session_state.stage == 202.1:
                show_nav(202.1)
                st.write("**Is it an acquisition?**")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202.1', {})
                choice = st.radio("Select if it is an acquisition:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": set_stage(202.3)
                    else: set_stage(203)

            elif st.session_state.stage == 202.2:
                show_nav(202.2)
                st.write("Products from a Joint Venture must follow the parent company's brand.")
                if st.button("Show Recommendation"):
                    display_result('evaluate_parent_entity')

            elif st.session_state.stage == 202.3:
                show_nav(202.3)
                st.write("**Does the acquired brand have Negative Brand Equity?**")
                st.caption("E.g., known bad reputation, scandal, or safety failures.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage202.3', {})
                choice = st.radio("Select if it has negative equity:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('retire_rebrand')
                    else: set_stage(203)

            elif st.session_state.stage == 203:
                show_nav(203)
                st.write("**Could it harm BASF's reputation?**")
                st.caption("E.g., Controversial industry, channel conflict, or high-risk technology.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage203', {})
                choice = st.radio("Select if there is a potential for negative impact:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('independent_risk')
                    else: set_stage(204)

            elif st.session_state.stage == 204:
                show_nav(204)
                st.write("**Does a legal contract already decide the brand?**")
                st.caption("E.g., Joint Venture agreement, brand licence, or hazard communication and labelling regulation.")
                options = ["Yes", "No"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage204', {})
                choice = st.radio("Select if a contract decides the brand:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "Yes": display_result('legal_directive')
                    else: set_stage(205)

            elif st.session_state.stage == 205:
                show_nav(205)
                st.write("**Does it have dedicated Brand Management resources?**")
                st.caption("This means multi-year budget and team for design, research, and brand management — not just product marketing.")
                options = ["No", "Yes"]
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage205', {})
                choice = st.radio("Select if resources are dedicated:", options,
                                  index=demo_data.get('index'), label_visibility="collapsed")
                if st.button("Proceed"):
                    if choice == "No": display_result('insufficient_resources')
                    else: set_stage(206)

            elif st.session_state.stage == 206:
                show_nav(206)
                st.caption("The product has passed all Fast Tracks. Score its strategic value and its need for a distinct brand.")
                demo_data = DEMO_DATA.get(st.session_state.demo_key, {}).get('stage206', {})
                rec_A = demo_data.get('score_A_checks', {})
                rec_B = demo_data.get('score_B_checks', {})
                rec_data = demo_data.get('data_mandate', "")

                questions_A = {
                    'pa1': "A) Business Strategy: Is this product, service or solution linked to a top priority of BASF's business strategy?",
                    'pa2': "B) Brand Building: Does this product, service or solution create a positive reputation impact for the BASF brand?",
                    'pa3': "C) Market Opportunity: Does this product, service or solution help us win in a new market, segment, or business model?",
                    'pa4': "D) Commercial Potential: Does this product, service or solution have proven high revenue or margin potential?",
                    'pa5': "E) Future Value: Does this product, service or solution represent a breakthrough innovation?"
                }
                questions_B = {
                    'pb1': "A) Portfolio Clarity: Does this product, service or solution need its own brand to avoid confusing customers or competing with other BASF products?",
                    'pb2': "B) Customers: Does this product, service or solution need to sell directly to end-customers using specific consumer marketing?",
                    'pb3': "C) Competitors: Does this product, service or solution compete primarily against specialised players?",
                    'pb4': "D) Marketing: Does this product, service or solution require a unique, agile, or highly specialised go-to-market approach?",
                    'pb5': "E) BASF Reputation: Is there any negative perception of the BASF brand among the target audience or in the market where this product, service, or solution will be deployed?"
                }

                examples_pA = {
                    'pa1': "E.g. It enhances our footprint in high-growth markets. It reinforces our leading cost position in key value chains. It improves reliability and product quality. It provides greater strategic and operational flexibility. It increases our ability to supply local markets. It enables our green transformation.",
                    'pa2': "E.g. Improves our reputation in areas such as sustainability, innovation, customer understanding, quality, reliability, ethical practices, safety, technological leadership, and market expertise.",
                    'pa3': "E.g. It provides access to a previously untapped region or a new customer segment. It helps us target markets further along the supply chain. It allows us to form new strategic partnerships. It allows us to compete in an innovative, high-potential field.",
                    'pa4': "E.g. It allows us to service a new segment or client type. It's an innovative, proprietary or patented solution. A high-margin specialty product. Has premium pricing potential. It generates strong recurring revenues. Can unlock upsell or cross-sell opportunities. It's a niche solution with limited competition.",
                    'pa5': "E.g. It represents a technological leap or game-changing customer solution. It is the result of a novel process or production technique. It creates a new market where none existed before. Offers radical improvement in cost-efficiency. It is a disruptive innovation that changes the expectations of the category. It's the first solution of its kind in the market."
                }
                examples_pB = {
                    'pb1': "E.g. It targets the same segment, for the same need, with a different solution. It solves the same customer issue, but in a technically different way. It represents a new or significantly improved version of an existing product. It addresses a general problem but for a different customer segment or group.",
                    'pb2': "E.g. It bypasses intermediaries and sells its offer directly to final buyers or through distributors. It relies on consumer-focused channels and messaging in order to reach and appeal to its audience.",
                    'pb3': "E.g. Competitors are narrowly focused on one specific area. They have category-specific value propositions and include category codes in their identity. They target narrowly defined audience segments through tailored messaging, category-specific channels and using a dedicated brand.",
                    'pb4': "E.g. Go to market involves rapid iteration or continuous feedback cycles; sales efforts are highly complex. The offer's value proposition is highly technical; distribution, sales, and communication happens through highly specialised channels.",
                    'pb5': "E.g. For this audience/in this market BASF is perceived as 'slow-moving', 'operationally complex', having a large 'environmental footprint', 'exposed to market risk', too 'chemically focused', 'excessively diversified', etc."
                }

                score_A, score_B = 0, 0
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Part A: Strategic Contribution**")
                    for key, q_text in questions_A.items():
                        if st.checkbox(q_text, value=rec_A.get(key, False), key=key):
                            score_A += WEIGHTS['product_A'][key]
                        with st.expander("See examples"):
                            st.caption(examples_pA[key])
                    st.session_state.scores['A'] = score_A
                    st.write(f"**Score A: {score_A} / 11**")
                with col2:
                    st.info("**Part B: Market Distinction**")
                    st.caption("Points are only awarded if supporting data is provided.")
                    for key, q_text in questions_B.items():
                        is_checked = st.checkbox(q_text, value=rec_B.get(key, False), key=key)
                        with st.expander("See examples"):
                            st.caption(examples_pB[key])
                        data_provided = st.text_area(
                            "Evidence / Data:", height=50, key=f"data_{key}",
                            value=rec_data if rec_B.get(key) else ""
                        )
                        if is_checked and data_provided.strip():
                            score_B += WEIGHTS['product_B'][key]
                        elif is_checked and not data_provided.strip():
                            st.warning("Provide evidence to receive points.", icon="⚠️")
                    st.session_state.scores['B'] = score_B
                    st.write(f"**Score B: {score_B} / 11**")

                if st.button("Calculate Recommendation"):
                    set_stage(207)

            elif st.session_state.stage == 207:
                score_a, score_b = st.session_state.scores['A'], st.session_state.scores['B']
                score_a_high = score_a >= HIGH_THRESHOLD
                score_b_high = score_b >= HIGH_THRESHOLD
                outcome_key = ''
                if score_a_high and score_b_high: outcome_key = 'product_endorsed'
                elif not score_a_high and score_b_high: outcome_key = 'flag_review'
                else: outcome_key = 'product_led'
                display_result(outcome_key)


# --- App Execution ---
if check_password():
    run_app()
