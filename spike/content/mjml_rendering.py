from copy import copy
from functools import lru_cache
from textwrap import dedent

import mrml
from django.utils.html import escape
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.rich_text import EmbedRewriter, LinkRewriter, MultiRuleRewriter, RichText, features
from wagtail.rich_text.pages import PageLinkHandler


class LinkHandlerForEmail(PageLinkHandler):
    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            page = cls.get_instance(attrs)
            return '<a href="%s">' % escape(page.localized.specific.full_url)
        except Page.DoesNotExist:
            return "<a>"


@lru_cache(maxsize=None)
def get_rewriter_for_email():
    embed_rules = copy(features.get_embed_types())
    link_rules = copy(features.get_link_types())
    link_rules["page"] = LinkHandlerForEmail
    return MultiRuleRewriter(
        [
            LinkRewriter(
                {
                    linktype: handler.expand_db_attributes
                    for linktype, handler in link_rules.items()
                },
            ),
            EmbedRewriter(
                {
                    embedtype: handler.expand_db_attributes
                    for embedtype, handler in embed_rules.items()
                },
            ),
        ]
    )


def rewrite_db_html_for_email(rich_text):
    rewriter = get_rewriter_for_email()
    return rewriter(rich_text.source)


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
                      {rewrite_db_html_for_email(rich_text)}
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
