IF (BUILD_GUI)
    PYSIDE_WRAP_RC(Plot_QRC_SRCS resources/Plot.qrc)
ENDIF (BUILD_GUI)

SET(PlotMain_SRCS
    InitGui.py
    PlotGui.py
)
SOURCE_GROUP("" FILES ${PlotMain_SRCS})

SET(PlotAxes_SRCS
    plotAxes/__init__.py
    plotAxes/TaskPanel.py
)
SOURCE_GROUP("plotaxes" FILES ${PlotAxes_SRCS})

SET(PlotLabels_SRCS
    plotLabels/__init__.py
    plotLabels/TaskPanel.py
)
SOURCE_GROUP("plotlabels" FILES ${PlotLabels_SRCS})

SET(PlotPositions_SRCS
    plotPositions/__init__.py
    plotPositions/TaskPanel.py
)
SOURCE_GROUP("plotpositions" FILES ${PlotPositions_SRCS})

SET(PlotSave_SRCS
    plotSave/__init__.py
    plotSave/TaskPanel.py
)
SOURCE_GROUP("plotsave" FILES ${PlotSave_SRCS})

SET(PlotSeries_SRCS
    plotSeries/__init__.py
    plotSeries/TaskPanel.py
)
SOURCE_GROUP("plotseries" FILES ${PlotSeries_SRCS})

SET(all_files ${PlotMain_SRCS} ${PlotAxes_SRCS} ${PlotLabels_SRCS} ${PlotPositions_SRCS} ${PlotSave_SRCS} ${PlotSeries_SRCS})

SET(PlotGuiIcon_SVG
    resources/icons/Plot_Workbench.svg
)

ADD_CUSTOM_TARGET(Plot ALL
    SOURCES ${all_files} ${Plot_QRC_SRCS} ${PlotGuiIcon_SVG}
)

fc_copy_sources(Plot "${CMAKE_BINARY_DIR}/Mod/Plot" ${all_files})

fc_copy_sources(Plot "${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_DATADIR}/Mod/Plot" ${PlotGuiIcon_SVG})

IF (BUILD_GUI)
    fc_target_copy_resource(Plot
        ${CMAKE_CURRENT_BINARY_DIR}
        ${CMAKE_BINARY_DIR}/Mod/Plot
        Plot_rc.py)
ENDIF (BUILD_GUI)

INSTALL(
    FILES
        ${PlotAxes_SRCS}
    DESTINATION
        Mod/Plot/plotAxes
)
INSTALL(
    FILES
        ${PlotLabels_SRCS}
    DESTINATION
        Mod/Plot/plotLabels
)
INSTALL(
    FILES
        ${PlotPositions_SRCS}
    DESTINATION
        Mod/Plot/plotPositions
)
INSTALL(
    FILES
        ${PlotSave_SRCS}
    DESTINATION
        Mod/Plot/plotSave
)
INSTALL(
    FILES
        ${PlotSeries_SRCS}
    DESTINATION
        Mod/Plot/plotSeries
)
INSTALL(
    FILES
        ${PlotMain_SRCS}
        ${Plot_QRC_SRCS}
    DESTINATION
        Mod/Plot
)
INSTALL(
    FILES
        ${PlotGuiIcon_SVG}
    DESTINATION
        "${CMAKE_INSTALL_DATADIR}/Mod/Plot/resources/icons"
)
