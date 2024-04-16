from textwrap import dedent

import mrml
from wagtail.images.models import Image
from wagtail.rich_text import RichText


def render(rich_text=RichText("")):
    return mrml.to_html(
        dedent(
            f"""
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
                      {rich_text}
                    </mj-text>
                  </mj-column>
                </mj-section>

                <mj-section>
                  <mj-column>
                    <mj-text>
                        --- begin custom footer ---
                        <a href="*|UNSUB|*">Unsubscribe</a>
                        Our mailing address is:<br />

                        *|HTML:LIST_ADDRESS_HTML|*<br />

                        *|IF:REWARDS|* *|HTML:REWARDS|* *|END:IF|*
                        --- end custom footer ---
                    </mj-text>
                  </mj-column>
                </mj-section>
              </mj-body>
            </mjml>
            """
        )
    )


def get_rich_text():
    image = Image.objects.first()

    return RichText(
        dedent(
            f"""\
            <h1>Heading 1</h1>

            <h2>Heading 2</h2>

            <h3>Heading 3</h3>

            <h4>Heading 4</h4>

            <h5>Heading 5</h5>

            <h6>Heading 6</h6>

            <ol>
                <li>OL1</li>
                <li>OL2</li>
            </ol>

            <ul>
                <li>UL1</li>
                <li>UL2</li>
            </ul>

            <blockquote>Blockquote</blockquote>

            <p>
                <a href="https://docs.wagtail.org">External link</a>
            </p>

            <p>
                <a linktype="page" id="3">Internal link</a>
            </p>

            <embed
                embedtype="image"
                format="fullwidth"
                id="{image.pk}"
                alt="Wagtail Mail"
            />

            <hr/>
            """
        )
    )
