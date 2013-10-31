from django.contrib.auth.admin import UserAdmin
from main.actions import export_select_fields_csv_action

UserAdmin.list_per_page = 1000
UserAdmin.list_max_show_all = 1000
UserAdmin.actions = [
    export_select_fields_csv_action("Get Users",
                                    fields=[
                                        ('first_name', 'First Name'),
                                        ('last_name', 'Last Name'),
                                        ('email', 'Email'),
                                        ],
                                    header=True
    )]
