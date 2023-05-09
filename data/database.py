
def create_db(engine, drop_first=True):
    """
    Creates tables if the engine has the privilege to do so

    :param engine:
    :param drop_first:
    :return:
    """
    if drop_first:
        engine.metadata.drop_all(engine.get_engine())
    engine.metadata.create_all(engine.get_engine())

    pass
