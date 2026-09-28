from premailer import transform
html = '<a href="{% url \'dashboard\' %}" class="btn">Click {{ user.name }}</a>'
print(transform(html))
