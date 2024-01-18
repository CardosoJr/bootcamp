from vizro import Vizro
import vizro.models as vm
import vizro.plotly.express as px

page=vm.Page(
    title="Example Dashboard",
    components=[
        vm.Graph(figure=px.scatter(
            px.data.iris(),
            title="Scatter",
            x="sepal_length",
            y="petal_width",
            color="species")),
        vm.Graph(figure=px.histogram(
            px.data.iris(),
            title="Histogram",
            x="sepal_length",
            color="species"))],
    controls=[
        vm.Filter(column="species"),
        vm.Filter(column="sepal_length"),
        vm.Filter(column="petal_width")])

Vizro().build(vm.Dashboard(pages=[page])).run()