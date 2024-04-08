import statsmodels.api as sm
import statsmodels.formula.api as smf

def train_lin_reg(df):
    model = smf.ols("Price ~ Rooms + Distance + Propertycount", df).fit()
    return model