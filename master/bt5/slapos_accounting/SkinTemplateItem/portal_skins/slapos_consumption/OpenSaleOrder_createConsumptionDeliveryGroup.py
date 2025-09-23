if activate_kw is None:
  activate_kw = {}

portal = context.getPortalObject()
open_sale_order = context

consumption_delivery_group = portal.consumption_delivery_group_module.newContent(
  portal_type="Consumption Delivery Group",
  title=title,
  #reference=
  #grouping_reference=
  follow_up=open_sale_order.getSourceProject(),
  start_date=current_date
)

consumption_delivery_group.open()
