from mjml import mjml2html

TEMPLATE = """
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-image width="100px" src="/assets/img/logo-small.png"></mj-image>
        <mj-divider border-color="#F45E43"></mj-divider>
        <!-- Say hello to the user -->
        <mj-text font-size="20px" color="#F45E43" font-family="Open Sans">Hello World</mj-text>
      </mj-column>
    </mj-section>
    <mj-section>
      <mj-column>
        <mj-social font-size="15px" icon-size="30px" mode="horizontal">
          <mj-social-element name="facebook" href="https://mjml.io/">
            Facebook
          </mj-social-element>
          <mj-social-element name="google" href="https://mjml.io/">
            Google
          </mj-social-element>
          <mj-social-element  name="twitter" href="https://mjml.io/">
            Twitter
          </mj-social-element>
        </mj-social>
      </mj-column>
    </mj-section>
    <mj-section>
      <mj-column>
        <mj-text>
            --- begin custom footer ---

            <p>*|LIST:DESCRIPTION|* <br />

            <br />

            <a href="*|UNSUB|*">Unsubscribe</a> *|EMAIL|* from this list.<br />

            <br />

            Our mailing address is:<br />

            *|HTML:LIST_ADDRESS_HTML|*<br />

            <br />

            Copyright (C) *|CURRENT_YEAR|* *|LIST:COMPANY|* All rights reserved.<br />

            <br />

            <a href="*|FORWARD|*">Forward</a> this email to a friend<br />

            <a href="*|UPDATE_PROFILE|*">Update your preferences</a><br />

            <br />

            *|IF:REWARDS|* *|HTML:REWARDS|* *|END:IF|*</p>

            --- end custom footer ---
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
"""

def render(src=TEMPLATE):
    return mjml2html(src)
