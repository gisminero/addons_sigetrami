@api.model
def create(self, vals):
    result = super(HrExpenseAdvances, self).create(vals)
    group_hr_expense_manager_id = self.env['ir.model.data'].xmlid_to_res_id('hr_expense.group_hr_expense_manager')
    hr_expense_managers = self.get_users_from_group(group_hr_expense_manager_id)
    if hr_expense_managers:
        result.message_subscribe_users(user_ids=hr_expense_managers)
    return result


# passing group id using self.env['ir.model.data'].xmlid_to_res_id('hr_expense.group_hr_expense_manager')
@api.multi
def get_users_from_group(self, group_id):
    users_ids = []
    sql_query = """select uid from res_groups_users_rel where gid = %s"""
    params = (group_id,)
    self.env.cr.execute(sql_query, params)
    results = self.env.cr.fetchall()
    for users_id in results:
        users_ids.append(users_id[0])
    return users_ids