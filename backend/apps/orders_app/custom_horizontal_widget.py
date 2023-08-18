from django.forms import CheckboxSelectMultiple, SelectMultiple


class CustomHorizontalWidget(CheckboxSelectMultiple):
    template_name = 'admin/widgets/custom_horizontal_widget.html'
