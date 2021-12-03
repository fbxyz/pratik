import numpy as np
from scipy import stats

# Fonction test des moyennes et variances
def test_moyenne(x, y, pval_only=False):
    """
    @return: str
    @type x: np.array
    @type y: np.array
    """
    # Normality test
    sv_x, sp_x = stats.shapiro(x)
    sv_y, sp_y = stats.shapiro(y)

    if sp_x < 0.05 or sp_y < 0.05:
        var = "H1"
        test_n = "Au moins une distribution ne suit pas une loi normale"

    else:
        var = "H0"
        test_n = ""

    # Variance test
    if var == 'H0':
        vv, vp = stats.bartlett(x, y)
        if vp < 0.05:
            test_v = f"Les écart-types sont significativement différents:<br>{np.std(x):.3f} et {np.std(y):.3f}, p= {vp:.4f}"
        else:
            test_v = f"Les écart-types ne sont pas significativement différents:<br>{np.std(x):.3f} et {np.std(y):.3f}, p= {vp:.4f}"

    else:
        vv, vp = stats.levene(x, y)
        if vp < 0.05:
            test_v = f"Les écart-types sont significativement différents:<br>{np.std(x):.3f} et {np.std(y):.3f}, p= {vp:.4f}"
        else:
            test_v = f"Les écart-types ne sont pas significativement différents:<br>{np.std(x):.3f} et {np.std(y):.3f}, p= {vp:.4f}"

    # mean test
    if vp >= 0.05:
        tv, tp = stats.ttest_ind(x, y, equal_var=True)
    else:
        tv, tp = stats.ttest_ind(x, y, equal_var=False)  # Welch

    if tp >= 0.05:
        test_m = f"Les moyennes ne sont pas significativement différentes:<br>{np.mean(x):.3f} et {np.mean(y):.3f}, p= {tp:.4f}"
    else:
        test_m = f"Les moyennes sont significativement différentes:<br>{np.mean(x):.3f} et {np.mean(y):.3f}, p= {tp:.4f}"
        
    if pval_only == False :
        return test_n + '<br>' + test_v + '<br>' + test_m
    
    else :
        return {"Moyenne x" :np.rint(np.mean(x)), "Var x" :np.rint(np.std(x)),
                "Moyenne y" :np.rint(np.mean(y)), "Var y" :np.rint(np.std(y)),
                "p-value Moyenne" :np.around(tp,2), "p-value Var" :np.around(vp,2)}

