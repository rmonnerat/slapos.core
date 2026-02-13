assert project.getPortalType() == 'Project'

# Compatible with ERP5User_getUserSecurityCategoryValueList
for entry in context.ERP5User_getSecurityCategoryValueFromAssignment(
  rule_dict={
    ('destination_project', ): ((), ),
  },
):
  # KeyError ?
  found_project = entry['destination_project'][0][0]
  if found_project.getUid() == project.getUid():
    return True
