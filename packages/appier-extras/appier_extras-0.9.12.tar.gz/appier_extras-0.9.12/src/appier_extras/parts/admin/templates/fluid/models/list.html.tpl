{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Admin{% endblock %}
{% block name %}Site administration{% endblock %}
{% block content %}
    <div>
        {% for section, models in models_d.items() %}
            {% set available = own._available(models) %}
            {% if available|length > 0 %}
                <div class="panel-model">
                    <h3>{{ section }}</h3>
                    <ul>
                        {% for model in available %}
                            {% if acl("admin.models." + model._name()) %}
                                <li>
                                    <div class="left">
                                        <a class="name" href="{{ url_for('admin.show_model', model = model._name()) }}">{{ model._name() }}</a>
                                    </div>
                                    <div class="right">
                                        <span class="button create" data-link="{{ url_for('admin.new_entity', model = model._name()) }}">create</span>
                                        <span class="button update" data-link="{{ url_for('admin.show_model', model = model._name()) }}">update</span>
                                    </div>
                                    <div class="clear"></div>
                                </li>
                            {% endif %}
                        {% endfor %}
                    </ul>
                 </div>
             {% endif %}
        {% endfor %}
    </div>
{% endblock %}
