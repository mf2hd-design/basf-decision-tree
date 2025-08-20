import streamlit as st
import base64

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


# --- SVG FLOWCHART ---
def render_svg(svg_string: str):
    """Renders the given SVG string in a pannable and zoomable container."""
    # Use base64 encoding to embed the SVG directly in the HTML
    b64 = base64.b64encode(svg_string.encode("utf-8")).decode("utf-8")
    html = f'''
    <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; overflow: auto; height: 600px; background-color: white;">
        <img src="data:image/svg+xml;base64,{b64}"/>
    </div>
    '''
    st.components.v1.html(html, height=620, scrolling=True)

flowchart_svg_string = """
<svg xmlns="http://www.w3.org/2000/svg" style="background: #ffffff; background-color: light-dark(#ffffff, var(--ge-dark-color, #121212)); color-scheme: light dark;" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="931px" height="1671px" viewBox="-0.5 -0.5 931 1671"><defs/><rect fill="#ffffff" width="100%" height="100%" x="0" y="0" style="fill: light-dark(#ffffff, var(--ge-dark-color, #121212));"/><g><g data-cell-id="0"><g data-cell-id="1"><g data-cell-id="3"><g><rect x="130" y="90" width="550" height="910" rx="82.5" ry="82.5" fill="#e6f2ff" stroke="none" pointer-events="all" style="fill: light-dark(rgb(230, 242, 255), rgb(22, 32, 43));"/></g><g><g><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe flex-start; width: 548px; height: 1px; padding-top: 97px; margin-left: 132px;"><div style="box-sizing: border-box; font-size: 0; text-align: left; color: #002B55; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: light-dark(#002B55, #aed3f7); line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; "><blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;"><blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">Phase 1: Qualification - The 'What'</blockquote></blockquote></div></div></div></foreignObject><image x="132" y="97.5" width="548" height="17" xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAACJAAAABECAYAAADUKl3EAAAQAElEQVR4AeydCZwcRdn/f9WzOTAEREwQBcGQl5CZzSKgnAIL4oEIgWRmE05RROR6VVARXoWgongA/gVBeUXQICQ7m3AECDfhkusNQrIzIVyiRsREEBICSXan6//UzO7sdHfNTM/u7Ozs7K8/VdNVTz11fau7enbrmWoHPEiABEiABEiABEiABEiABEiABEiABBqdAPtHAiRAAiRAAiRAAiRAAiRAAiRAAiTQ+ATYQxIYEAEakAwIHzOTAAmQAAmQAAmQAAmQAAmQQK0IsB4SIAESIAESIAESIAESIAESIAESIIHGJ8AekgAJkMDQEaABydCxZ80kQAIkQAIkQAIkQAIjtwD7TwIkQAIkQAIkQAIkQAIkQAIkQAIk0PgE2EMSIAESIAESGKYEaEAyTAeOzSYBEiABEiABEhgaAqyVBEiABEiABEiABEiABEiABEiABEig8QmwhyRAAiRAAiRAAiQwEgnQgGQkjjr7TAIkQAIjmwB7TwIkQAIkQAIkQAIkQAIkQAIkQAIk0PgE2EMSIAESIAESIAESIAESIIEKCdCApEJgVCcBEqgHAmwDCZAACZAACZAACZAACZAACZAACZBA4xNgD0mABEiABEiABEiABEiABEiABGpJgAYktaTNuvoIMEQCJEACJEACJEACJEACJEACJEACJEACJND4BNhDEiABEiABEiABEiABEiABEiABEiCBYUOg3wYkw6aHbCgJkAAJkAAJkAAJkAAJkAAJkAAJkEC/CTAjCZAACZAACZAACZAACZAACZAACZBA4xNgD0nAEKABiaFATwIkQAJDTaDlqIloPnqbvN/xxLHgQQLDlcC0Y7ZCc9tx4n+OWOKP4h8S/5L4f4lPIZq4W/wfxP8UzYmjsEdiy+Ha1WHf7snHboHozN0QjScQi38dsbbTEZv18WHfL3aABOqNwNA/5+uNSOO156NHvjf/Pc58pzPza+P1kj0iARIgARIgARIgARIgARIgARKobwJsHQmQAAkMmAANSAaMkAWQAAk0BIFdZu+IWEIP0P8d0cRtiLX9RBbOv5RdRAgDpyUxBZmmf0F3v5b34965MExW6pBA/RCY4yBrhJC4GW7XG9B6rvizpX3HiN9f/CTxE8VHofAp8ceL/xY0FmID3pR7705E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"/></switch></g></g></g></g><g data-cell-id="46"><g><path d="M 612.44 804.81 L 723.82 825.13" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke" style="stroke: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));"/><path d="M 728.92 826.43 L 722.95 828.6 L 723.82 825.13 L 721.28 822.14 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all" style="fill: light-dark(rgb(0, 0, 0), rgb(255, 255, 255)); stroke: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));"/></g><g data-cell-id="47"><g><g><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 814px; margin-left: 659px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; color: #000000; background-color: #ffffff; "><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: light-dark(#000000, #ffffff); line-height: 1.2; pointer-events: all; background-color: light-dark(#ffffff, var(--ge-dark-color, #121212)); white-space: nowrap; ">No</div></div></div></foreignObject><image x="652" y="808" width="14" height="15.75" xlink:href="data:image/png;base64,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"/></switch></g></g></g></g><g data-cell-id="50"><g><path d="M 648.06 805 L 723.7 890.32" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke" style="stroke: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));"/><path d="M 728.9 891.9 L 721.46 893.99 L 723.7 890.32 L 721.57 886.83 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all" style="fill: light-dark(rgb(0, 0, 0), rgb(255, 255, 255)); stroke: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));"/></g><g data-cell-id="51"><g><g><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 864px; margin-left: 686px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; color: #000000; background-color: #ffffff; "><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: light-dark(#000000, #ffffff); line-height: 1.2; pointer-events: all; background-color: light-dark(#ffffff, var(--ge-dark-color, #121212)); white-space: nowrap; ">Minority (&lt;50%)</div></div></div></foreignObject><image x="647.5" y="858" width="77" height="15.75" xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAATQAAAA/CAYAAABuMTToAAAQAElEQVR4AeydBZxcNRPA8/ohxd0ptLhT3OGKu7sWd3c/3Iu7FXd3b3GncA7FHQ53/fr/brOzs83WyV76azY2kTeZzGSSeR5v/Bv+BQwEDAQMNAkGerjwL2AgYCBgoEkwEAhaky5k+IyAgYAB5wJB61SzIHQlYCBgoDYMBIJWG/5C6YCBgIFOhIFA0DrRMITOBEzAQG0YCARtNeFv3+82d6FwLhAwELh3DAz47y9gA7t27XKcOHEirVq1klOnTsmhQ4cUcQ3Lly8XJAgL/tq1a+08H9Y4d+6cK1z9/f3l5s2bQ4v4fJ6P7x/uM8b3oW8y5pvg8/s93oV6gI87rL+U+b388ss+5zB8+HC972+88YZ8++23j1F//fVX24d45513ZMCAATpW/eCqVau2+y35PjE84P7222/ljjvuMN5717dvXw8xY0uXLlU/Wz4H64E0/bfffus2q1OnjqT78d9www2VnQ0j0F4Evvvuum28e+sI3Lp1q002b94cE0i/fv18YxJ7+PCh5FOnTpoQ5i+vI63aJp86dVKl93o5s3bLli164xT+E4j64L9w4UJp1Kghx9/Lg49fV4x80eWbb77J7uV69gP1O/h94Hn9sCgWLFgQPq/9R9oM7W1ddu7cKd26ddN89tprr3WbYt/E+b//+7+u+p/lY4c/9r+e/U4qI66nE30H/Y3A4315M4wKjB0F7R1X9V5jQJp50T6N5eHxeDxD0Gg0Wrt+w8b1c4V3hN0Z8S197eOPP1Y2k+g+6N7t3btX0sN0yO6jO7X+q896hI/oX8bVq1fH6P+gN9Vn+G66+X07bYx+P+D//u/vXqO9O+vWrePI89x0001+X4d+8cUX3rYcO3ZM0L56l/hX+uX7N99849E2K/b/dI72s8+fBwQ/N349y7s61p3O7+O8r8d8bA/n/VvO1xP+Xn7O/zH5n+369r0c4xX48X7aU3d5/eWf5N8Rz5f8W6v/hPwfW3/n9O+G72c918U/2f4/iU/sKz9i/U+/h+99f4937z/o3++f/W/q7/n8v/9xH/L/x/v6P//z8j/eX/f1/z/5n/z//3/jP+/7/3///+z//7/o/+3//R//D/+3/xf/X/5/9b/y//rf9f/oP/1f/D/4H/7P/l/+v/0P/V/+z/j/+f/1///z//Z//b/8/+/n/+L/9X/x//v/r//5//I/7/+b/4H/+///0H//8P8I+8v1YAAAAASUVORK5CYII="/></switch></g></g></g></g><g data-cell-id="48"><g><path d="M 598.05 921.2 L 723.82 865.34" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke" style="stroke: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));"/><path d="M 728.84 863.49 L 723.95 869.25 L 723.82 865.34 L 720.93 862.77 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all" style="fill: light-dark(rgb(0, 0, 0), rgb(255, 255, 255)); stroke: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));"/></g><g data-cell-id="49"><g><g><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 885px; margin-left: 661px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; color: #000000; background-color: #ffffff; "><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: light-dark(#000000, #ffffff); line-height: 1.2; pointer-events: all; background-color: light-dark(#ffffff, var(--ge-dark-color, #121212)); white-space: nowrap; ">Majority (&gt;=50%)</div></div></div></foreignObject><image x="622.5" y="879" width="77" height="15.75" xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAATQAAAA/CAYAAABuMTToAAAQAElEQVR4AeydBZxcNRPA8/ohxd0ptLhT3OGKu7sWd3c/3Iu7FXd3b3GncA7FHQ53/fr/brOzs83WyV76azY2kTeZzGSSeR5v/Bv+BQwEDAQMNAkGerjwL2AgYCBgoEkwEAhaky5k+IyAgYAB5wJB61SzIHQlYCBgoDYMBIJWG/5C6YCBgIFOhIFA0DrRMITOBEzAQG0YCARtNeFv3+82d6FwLhAwELh3DAz47y9gA7t27XKcOHEirVq1kps2b5L777/f7c9eS5YskXffffcchv0z584lpS0aW1E3w8aNG01O//zzz69c0O90rJ7bYg586tQp+f77732s7N6923X2G9zWvXv3tG/f3u/46NGj/Gk5e/YsR/cffvhBZs2aJbVr1xZl+tChQ+XixYtmXU8/9JgYx+7h/PnzE6b8v/nmm6a0b/PmzZKcnBylpaVlQ874+Hg+c5iRkSG9evWygD8oKChY7vWdO3dsjX7vvfe6vA0ePFrGjx+v83h0xP3atWvp3bu3zJ8/X2A0059+5h5dC6RWrVpSrVo1efrpp+14tS3t+tVXX2mY/vrrr6/P4w8ePMj3l19+sRQnO/oD/S2d5/j+P/nkk5R2O48++qg0bNiw1j9//vz+e8/Pz5e5c+d6y5vM+vXrpcu+p1XmY+J+j+8f9jFjY8n+5ZdfpL/88oua9J/WjWdO1q04w+M/q8c3n3/eeeedhL0yD4fWw4cPy7Rp03y7yX4EihYtKsePH48k6s6dO5qC31H063333Xd3bN/YjX51Q72vM/S/j/tP/e83Xf3Hh4/8P8f+uL/+H/t3//v9c+3/X/3n+7+P3/n+/j/yH9T+24/8h/1/6T/0H97/5f8//T/97//z/+/8n/R/+v91/j//R/+n/+1/+v/l/9b/y//+/j/u//J//j/8//Z//v/if/D/0v/k/+9/0P//T/+3/r/7H/v//p//T//P/+3/+X/i/+z//5/8//9//h//X/5f/Qf/n//cAv/q+rAAAAAElFTkSuQmCC"/></switch></g></g></g></g><g data-cell-id="50"><g><path d="M 649.52 795.34 L 723.75 899.41" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke" style="stroke: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));"/><path d="M 728.93 900.86 L 721.57 902.99 L 723.75 899.41 L 721.43 895.96 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all" style="fill: light-dark(rgb(0, 0, 0), rgb(255, 255, 255)); stroke: light-dark(rgb(0, 0, 0), rgb(255, 255, 255));"/></g><g data-cell-id="51"><g><g><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 863px; margin-left: 687px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; color: #000000; background-color: #ffffff; "><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: light-dark(#000000, #ffffff); line-height: 1.2; pointer-events: all; background-color: light-dark(#ffffff, var(--ge-dark-color, #121212)); white-space: nowrap; ">Minority (&lt;50%)</div></div></div></foreignObject><image x="648.5" y="857" width="77" height="15.75" xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAATQAAAA/CAYAAABuMTToAAAQAElEQVR4AeydBZxcNRPA8/ohxd0ptLhT3OGKu7sWd3c/3Iu7FXd3b3GncA7FHQ53/fr/brOzs83WyV76azY2kTeZzGSSeR5v/Bv+BQwEDAQMNAkGerjwL2AgYCBgoEkwEAhaky5k+IyAgYAB5wJB61SzIHQlYCBgoDYMBIJWG/5C6YCBgIFOhIFA0DrRMITOBEzAQG0YCARtNeFv3+82d6FwLhAwELh3DAz47y9gA7t27XKcOHEirVq1klOnTsmhQ4cUcQ3Lly8XJAgL/tq1a+08H9Y4d+6cK1z9/f3l5s2bQ4v4fJ6P7x/uM8b3oW8y5pvg8/s93oV6gI87rL+U+N3LL7/s85hjY1u3bv1V24f2b9SoUbrwwgudM68e0C3a/wULFiwK+n0u99xzT3fOOeeYxNupGDe8j9bA2/Jv+P/t//N/9D+g/gX+P+D//V/8v/if9H/s/3/5/+3/q//T/4H/7f/l/+P/1f/n/+L/+3/u//J/wn9Y/97/8v/t/8n/+H/p/+7//R/2H963/pf/rf8f/S/if9H/y/yv/T/7//5//o/99/3f+b/+P//v/Y//n/+n/eP+X//P/+X/Q/0b+f/w//f/+/+7/oP/1f/B/+n/+v/3/+f/2/+x/9X/7/+n/zP/9/fP/S//H/83/K/8v/sP//6f/t/+v/y/8x/+H/yv/v//P/p//D//v/2/8v/+P/4v/T//H/0//f//T/7//D/8f/S/+7/+d/1P97/8H/hP/j/+n/eP+n//7/5f+T//9/2P//3/N/8n/+P/2//L/4P//+4/a/eX6v/+/s/4f/L//v/sH/4/+H/v/8v/53+v/5P+0/7//D/3b/b/j/yH9X/bT/yH/f/sH/oH/b/2j/6D+/f8n/6/+//9J/939zP9/85f/9fvP//v/if/D/7/+T/5f/v/2v/8v/qf/h/87/x/+P/+X/6f/B/+7/+1/+X/wf8G/p/+3/+P/7f/x//D/2n/r//5/9z/1f/s/+P/5f/V/z//j//9/5v/g//X//p//s//p/+/8v/8n/+b//3//P/v//V/+H/gH//+T/9X/p/x/8b/z//l/9H/v/+f/+v+T/n/+f/g/4P/u//X/x//r//d/3v/R/+H/+/+r//j/1f/y//f/8/+v//3/+3/af/B//z/73/+/8f+H//H/tH//j//P/u//j//R/t/+z//l/wf/v//t/2n/w//T/7f/7//F/+n/wf/q/+7/+j/1f/9/eX/f/3//N/63//H/8v/+v+7/2f/R/9//6/9X/2f/B/+f/8f7H/+X/5f/y/3P/+f/q/+9/4P/S/+D/93/x//p/2X/oP/X//T/wf/o//X/4P/C/k3/T/yv/T/9f9a+f8fAAD//7kY7XAAAAAGSURBVAMAfJqR8r1hRkUAAAAASUVORK5CYII="/></switch></g></g></g></g></g></g></svg>
"""

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
            render_svg(flowchart_svg_string)
    
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
