<!DOCTYPE html>
<html lang="en">
<div>
  Status code:
  {% if data.responseCode %}
    {{ data.responseCode }}
  {% else %}
    None
  {% endif %}
</div>

{% if data.url %}
  <div>{{ data.url }}</div>
{% endif %}

{% if data.body %}
  <h4>Body</h4>
  <div>
    <pre class="preformated-text">{{ data.body }}</pre>
  </div>
{% endif %}

{% if data.headers %}
  <h4>Headers</h4>
  <div>
    {% for name, value in data.headers.items() %}
      <div>{{ name }}: {{ value or 'null' }}</div>
    {% endfor %}
  </div>
{% endif %}

{% if data.cookies %}
  <h4>Cookies</h4>
  <div>
    {% for name, value in data.cookies.items() %}
      <div>{{ name }}: {{ value or 'null' }}</div>
    {% endfor %}
  </div>
{% endif %}
</html>