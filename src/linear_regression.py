from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from matplotlib import pyplot
from os.path import join
from numpy import array
from pandas import (
    DataFrame,
    Series,
    read_csv,
)


def get_vector(
    data: Series,
) -> array:
    data = data.to_numpy()
    data = data.reshape(
        -1,
        1,
    )
    return data


def get_linear_regression(
    data: DataFrame,
) -> LinearRegression:
    input_ = get_vector(
        data["Optical_Method_mean"],
    )
    output_ = get_vector(
        data["Gravimetric_Method"],
    )
    model = LinearRegression(
        fit_intercept=False,
    )
    model = model.fit(
        input_,
        output_,
    )
    return model


def evaluate_model(
    model: LinearRegression,
    data: DataFrame,
) -> None:
    input_ = get_vector(
        data["Optical_Method_mean"],
    )
    output_ = get_vector(
        data["Gravimetric_Method"]
    )
    prediction = model.predict(
        input_,
    )
    r2 = r2_score(
        output_,
        prediction,
    )
    r2 = round(
        r2,
        3,
    )
    slope = model.coef_[0]
    slope = slope[0]
    print(
        f"R2 -> {r2}"
    )
    print(
        f"Slope -> {slope}"
    )


def prediction_model(
    model: LinearRegression,
    data: Series,
) -> Series:
    data_ = get_vector(
        data,
    )
    prediction = model.predict(
        data_,
    )
    prediction = prediction.flatten()
    prediction = Series(
        prediction,
    )
    prediction = DataFrame({
        "input": data,
        "output": prediction,
    })
    return prediction


filename = join(
    "..",
    "data",
    "propietary",
    "data.csv"


)
data = read_csv(
    filename,
    parse_dates=True,
    index_col=0,
    date_format="%d/%m/%Y",
)
fire_data = data[
    data["Gravimetric_Method"] >= 45
]
general_model = get_linear_regression(
    data,
)
fire_model = get_linear_regression(
    fire_data,
)
input_data = Series([
    0,
    180,
])
general_prediction = prediction_model(
    general_model,
    input_data,
)
fire_prediction = prediction_model(
    fire_model,
    input_data,
)
print("Modelo general")
evaluate_model(
    general_model,
    data,
)
print("Modelo para incendios")
evaluate_model(
    fire_model,
    fire_data,
)
pyplot.scatter(
    data["Optical_Method_mean"],
    data["Gravimetric_Method"],
    color="gray"
)
pyplot.scatter(
    fire_data["Optical_Method_mean"],
    fire_data["Gravimetric_Method"],
    color="black"
)
pyplot.plot(
    general_prediction["input"],
    general_prediction["output"],
    color="blue",
    lw=3,
)
pyplot.plot(
    fire_prediction["input"],
    fire_prediction["output"],
    color="red",
    lw=3,
)
pyplot.xlim(
    0,
    180,
)
pyplot.ylim(
    0,
    180,
)
pyplot.xlabel(
    "Optical method $(\\mu g/m^3)$"
)
pyplot.ylabel(
    "Gravimetric method $(\\mu g/m^3)$"
)
pyplot.savefig(
    "test.png"
)
