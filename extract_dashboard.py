import re

with open('/home/neon/bhavani_cashews/new_templates/admin_dashboard_bhavani_cashews_1/code.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract styles
style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
styles = style_match.group(1) if style_match else ''

# Extract content area
content_match = re.search(r'<div class="content-area">(.*?)</div>\s*</main>', html, re.DOTALL)
content = content_match.group(1) if content_match else ''

template = f"""{{% extends "admin/base_site.html" %}}
{{% load i18n static dashboard_tags %}}

{{% block extrastyle %}}
{{{{ block.super }}}}
<style>
{styles}
/* Override content padding to 0 since our content-area handles it */
#content {{ padding: 0 !important; background: var(--bg-deep) !important; }}
.content-area {{ padding: 32px; max-width: 1320px; margin: 0 auto; }}
</style>
{{% endblock %}}

{{% block coltype %}}colMS{{% endblock %}}

{{% block bodyclass %}}{{{{ block.super }}}} dashboard{{% endblock %}}

{{% block breadcrumbs %}}{{% endblock %}}

{{% block content %}}
{{% get_dashboard_data as dash_data %}}
<div id="content-main" style="display:block;">
  <div class="content-area">
    {content}
  </div>
</div>
{{% endblock %}}
"""

with open('/home/neon/bhavani_cashews/templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(template)

print('Extracted successfully')
