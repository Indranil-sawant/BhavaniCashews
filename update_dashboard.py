with open('/home/neon/bhavani_cashews/templates/admin/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace hardcoded values with Django template variables
replacements = {
    '<div class="kpi-value">$142,580</div>': '<div class="kpi-value">₹{{ dash_data.total_revenue|default:"0.00" }}</div>',
    '<div class="kpi-value">1,284</div>': '<div class="kpi-value">{{ dash_data.pending_shipments }}</div>',
    '<div class="kpi-value">03<span class="kpi-unit">Grades</span></div>': '<div class="kpi-value">{{ dash_data.low_stock_grades }}<span class="kpi-unit">Grades</span></div>',
    '<div class="kpi-value">4.9 / 5</div>': '<div class="kpi-value">{{ dash_data.quality_rating }} / 5</div>',
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open('/home/neon/bhavani_cashews/templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated successfully')
