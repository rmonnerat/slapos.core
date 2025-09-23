if context.getReference() is None:
  context.setReference(
    "CDG-%06d" % context.portal_ids.generateNewId(
        id_group="CDG",
        id_generator="uid",
        default=1))
