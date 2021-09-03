from wtforms import Form, StringField, SelectField


class ProductSearchForm(Form):
    search = StringField('')
