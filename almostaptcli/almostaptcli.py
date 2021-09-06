import argparse
from bson.json_util import dumps
import json
import pymongo
from pymongo.errors import OperationFailure
from rich import print
from rich.console import Console


console = Console()

try:
    conn_mongo_cli = 'YOUR MONGODB INSTANCE'

except pymongo.errors.ConnectionFailure() as err:
    print(f"[red] {err} [/] ")


db = conn_mongo_cli["tagroupdb"]

db_collection = db.tagroups

conn_mongo_cli.close()


def work_with_db_info(groupname) -> str:
    db_collection.create_index([("vendor_des", pymongo.TEXT), ("name", pymongo.TEXT)])

    threat_groups = db_collection.find(
        {"$text": {"$search": groupname}}, {"_id": False}
    )

    if not groupname:
        print(
            "[red] That group may not yet have been added, or doesnt exist. Try again..."
        )

    results = [entry for entry in threat_groups]

    json_data = dumps(results, indent=2)

    console.print(json_data, highlight=False)


def get_all_results_db():

    results_file = "tagroup_info.json"

    all_results = db_collection.find({}, {"_id": False})

    result = [x for x in all_results]

    print(f"[yellow] {len(result)} results found! [/] \n")

    with open(results_file, "w") as outfile:
        json.dump(result, outfile)

    print(f"[green] Results successfully written to {results_file}! [/]")

    # all_option_data = dumps(result, indent=2)

    # console.print(all_option_data, highlight=False)


def main():

    banner = """
    _   _              _     _   ___ _____ ___ _    ___  
   /_\ | |_ __  ___ __| |_  /_\ | _ \_   _/ __| |  |_ _| 
  / _ \| | '  \/ _ (_-<  _|/ _ \|  _/ | || (__| |__ | |  
 /_/ \_\_|_|_|_\___/__/\__/_/ \_\_|   |_| \___|____|___|                                                
 
Almost APT Command Line Program
----------------------------------------------------------------
This script will interact with the MongoDB instance to display information on lesser known threat actors. 
Use: include the group designator, or 'all' to display the entire collection. 

Examples:
\t python almostaptcli.py -g GROUPNAME
\t python almostaptcli.py -a ALL

"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=banner,
    )
    parser.add_argument("-g", "--groupname", help="Name of group to lookup")
    parser.add_argument("-a", "--all", help="Return all records", action="store_true")

    args = parser.parse_args()

    if args.groupname:
        try:
            conn_mongo_cli.server_info()
            print("[green] Connection established! [/ ]")
            print()
        except OperationFailure as err:
            print(f"[red] {err} [/] ")
        work_with_db_info(args.groupname)
    elif args.all:
        get_all_results_db()


if __name__ == "__main__":
    main()

