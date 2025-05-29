from gitch.core import gitch_commit

try:
    gitch_commit("First Gitch Devlog", False, True)
except Exception as e:
    import traceback
    traceback.print_exc()