from flask_wtf import FlaskForm
from wtforms.validators import Required

from atst.forms.fields import SelectField
from atst.utils.localization import translate

from .data import WORKSPACE_ROLES


class EditMemberForm(FlaskForm):
    # This form also accepts a field for each environment in each application
    #  that the user is a member of

    portfolio_role = SelectField(
        translate("forms.edit_member.portfolio_role_label"),
        choices=WORKSPACE_ROLES,
        validators=[Required()],
    )
