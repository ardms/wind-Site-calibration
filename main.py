# -*- coding: utf-8 -*-
"""
Created on 2024/11/18

@author: adimopoulos
"""

# from textual.app import App
import logging
import json
from rich.logging import RichHandler
from modules.schema import MetMast, Site


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")

with open("./config.json") as conf_file:
    conf = json.load(conf_file)

met_masts = []
for metmast in ["PMM", "CMM"]:
    MM = MetMast(
        name=f"{metmast}_T03",
        anemometers=conf[metmast]["anemometers"],
        vanes=conf[metmast]["vanes"],
        thermometers=conf[metmast]["thermometers"],
        **conf[metmast]["data"],
    )
    MM.load_timeseries_from_folder()

    MM.calculate_alpha(
        conf[metmast]["filter"]["AlphaLow"], conf[metmast]["filter"]["AlphaHigh"]
    )
    MM.calculate_TI()
    MM.calculate_upflow()

    MM_filter = conf[metmast]["filter"]
    MM.filter_timeseries_IEC(MM_filter)
    MM.filter_timeseries_add(MM_filter)
    MM.calculate_dir_bins(MM_filter)
    met_masts.append(MM)
    log.info(f"Met Mast {MM.name} has been added to met_mast list")

site_name = Site(name="Stranoch", PMM=met_masts[0], CMM=met_masts[1])
log.info(f"Site with name site_name has been created")
site_name.join_timeseries()
site_name.linear_regression()
breakpoint()
