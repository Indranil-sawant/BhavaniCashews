with open('/home/neon/bhavani_cashews/templates/admin/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the Recent Orders table body
table_body_start = html.find('<tbody>')
table_body_end = html.find('</tbody>') + len('</tbody>')

if table_body_start != -1 and table_body_end != -1:
    new_table_body = """<tbody>
            {% for order in dash_data.recent_orders %}
            <tr>
              <td>
                <div class="order-id">#ORD-{{ order.id|stringformat:"s"|slice:":8" }}</div>
              </td>
              <td>
                <div class="destination-city">{{ order.shipping_address.city|default:"Unknown" }}, {{ order.shipping_address.country|default:"India" }}</div>
                <div class="destination-method">{{ order.get_payment_method_display }}</div>
              </td>
              <td>
                <div class="grade-badge">Mixed</div>
              </td>
              <td>
                <div class="order-total">₹{{ order.total }}</div>
              </td>
              <td>
                {% if order.status == 'PLACED' or order.status == 'CONFIRMED' %}
                <div class="status-pill status-processing">
                  <span class="status-dot"></span> {{ order.get_status_display }}
                </div>
                {% elif order.status == 'SHIPPED' %}
                <div class="status-pill status-shipped">
                  <span class="status-dot"></span> {{ order.get_status_display }}
                </div>
                {% elif order.status == 'DELIVERED' %}
                <div class="status-pill status-delivered">
                  <span class="status-dot"></span> {{ order.get_status_display }}
                </div>
                {% else %}
                <div class="status-pill status-processing" style="background:var(--bg-surface);color:var(--text-muted);">
                  <span class="status-dot" style="background:var(--text-muted);"></span> {{ order.get_status_display }}
                </div>
                {% endif %}
              </td>
            </tr>
            {% empty %}
            <tr>
              <td colspan="5" style="text-align:center;color:var(--text-muted);padding:24px;">No recent orders.</td>
            </tr>
            {% endfor %}
          </tbody>"""
    html = html[:table_body_start] + new_table_body + html[table_body_end:]

# Replace the Inventory Grades
inventory_grades_start = html.find('<div class="inventory-grades">')
inventory_grades_end = html.find('</div>\n\n            <button class="inventory-btn">', inventory_grades_start)

if inventory_grades_start != -1 and inventory_grades_end != -1:
    new_inventory_grades = """<div class="inventory-grades">
              {% for grade in dash_data.inventory_grades %}
              <div class="grade-item">
                <div class="grade-item-header">
                  <span class="grade-name">{{ grade.name }}</span>
                  <span class="grade-qty">{{ grade.total_stock }} kg</span>
                </div>
                <div class="grade-bar-track">
                  {% if grade.total_stock > 500 %}
                  <div class="grade-bar-fill healthy" style="width: 100%;"></div>
                  {% elif grade.total_stock > 200 %}
                  <div class="grade-bar-fill warning" style="width: 60%;"></div>
                  {% else %}
                  <div class="grade-bar-fill critical" style="width: 25%;"></div>
                  {% endif %}
                </div>
                {% if grade.total_stock > 500 %}
                <div class="grade-status healthy">OPTIMAL STOCK LEVEL</div>
                {% elif grade.total_stock > 200 %}
                <div class="grade-status warning">RESTOCK RECOMMENDED</div>
                {% else %}
                <div class="grade-status critical">CRITICAL LEVEL - IMMEDIATE PROCESSING</div>
                {% endif %}
              </div>
              {% endfor %}
            </div>"""
    html = html[:inventory_grades_start] + new_inventory_grades + html[inventory_grades_end + 6:] # +6 to skip </div>

with open('/home/neon/bhavani_cashews/templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated table and inventory successfully')
