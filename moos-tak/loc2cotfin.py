# Jordan Beason 01/22/2024
# loc2cot subscribes to moos NODE_REPORT messages, and publishes their name and location via Cursor on Target to an ATAK network of your choosing.

import pymoos
import asyncio
import xml.etree.ElementTree as ET
from configparser import ConfigParser
import pytak

message_queue = asyncio.Queue()

class MySerializer(pytak.QueueWorker):
    """
    Defines how you process or generate your Cursor on Target Events.
    From there it adds the CoT Events to a queue for TX to a COT_URL.
    """
    async def process_messages(self):        
        while True:
            message = await message_queue.get()  # Get a message from MOOS
            if message:
                report_string = message.string() 
                data = parse_node_report(report_string) # Parse the node report into a data array
                cot = gen_cot(data) # Generate a COT message using the data array
                await self.put_queue(cot) # Put COT message in a publish queue
                await asyncio.sleep(.2)
            else:
                # If no message, you might want to wait for a bit or handle it differently
                await asyncio.sleep(.1)

            
    async def run(self, number_of_iterations=-1):
        """Run the loop for processing or generating pre-CoT data."""
        while 1:
            await self.process_messages()


def parse_node_report(report_string): # Splits the node report into its different data types and titles such as NAME and LAT LON
    data = {}
    try:
        pairs = report_string.split(',')
        for pair in pairs:
            key, value = pair.split('=')
            data[key] = value
    except Exception as e:
        print(f"Error parsing node report: {str(e)}, String: {report_string}")
    return data


def on_mail(): # Places MOOS NODE_REPORT in the message_queue starting the process_messages function
    try:
        for message in comms.fetch():
            if message.name() == 'NODE_REPORT':
                asyncio.run(message_queue.put(message))  # Put the message into the queue.
    except Exception as e:
        print(f"Error in on_mail: {str(e)}")
    return True

def on_connect(): # MOOS comms register for NODE_REPORT messages
    try:
        comms.register('NODE_REPORT', 0)
    except Exception as e:
        print(f"Error in on_connect: {str(e)}")
    return True
    

def gen_cot(data): # Generate the COT messages using parsed NAME, LAT, LON data from NODE_REPORT
    """Generate CoT Event."""
    name = data['NAME']
    root = ET.Element("event")
    root.set("version", "2.0")
    if name.startswith("blue"): # If the boat name starts with blue or red, set the COT message type as friend or foe
        root.set("type", "a-f-S-120700") #https://www.mitre.org/sites/default/files/pdf/09_4937.pdf
    elif name.startswith("red"):
        root.set("type", "a-h-S-120700")
    else 
        root.set("type", "t-x-d-d")
    root.set("uid", "AISC_OAI_" + name) # 
    root.set("how", "m-g")
    root.set("time", pytak.cot_time())
    root.set("start", pytak.cot_time())
    root.set(
        "stale", pytak.cot_time(60)
    )  # time difference in seconds from 'start' when stale initiates

   
    pt_attr = {
        "lat": str(data['LAT']),  # set your lat (this loc points to Central Park NY)
        "lon": str(data['LON']),  # set your long (this loc points to Central Park NY)
        "hae": "9999",
        "ce": "9999", # I believe these are confidence intervals
        "le": "9999",
    }

    ET.SubElement(root, "point", attrib=pt_attr) # Point message type

    return ET.tostring(root)

comms = pymoos.comms() #COMMS CONFIG
comms.set_on_connect_callback(on_connect)
comms.set_on_mail_callback(on_mail)
comms.run('localhost',9000,'pymoos')
config = ConfigParser()
config["mycottool"] = {"COT_URL": "tcp://137.184.101.250:8087"} #SET YOUR NETWORK INFO HERE
config = config["mycottool"]



async def main():
    """Main definition of your program, sets config params and
    adds your serializer to the asyncio task list.
    """
    # Initializes worker queues and tasks.
    clitool = pytak.CLITool(config)
    await clitool.setup()
    # Add your serializer to the asyncio task list.
    clitool.add_tasks(set([MySerializer(clitool.tx_queue, config)]))
    # Start all tasks.
    await clitool.run()

try:
    while True:
        pass
        if __name__ == "__main__":
            asyncio.run(main())
except KeyboardInterrupt:
    print("Terminating...")
    

