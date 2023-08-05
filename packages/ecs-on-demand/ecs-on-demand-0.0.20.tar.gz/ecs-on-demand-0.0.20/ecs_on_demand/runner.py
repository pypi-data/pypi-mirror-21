import os
import sys
import re
import boto3
import botocore


event_fields = tuple([
	"image",
	"task_role_arn",
	"privileged",
	"cluster",
	"count",
	"throughput",
])

bad_image_chars = re.compile(r"[/.]")

def _get_name_from_image(image):
	return bad_image_chars.sub("_", image)

def run(event, debug=False):

	event_name = _get_name_from_image(event["image"])

	region = event.get("region", os.environ.get("AWS_REGION"))
	logs = boto3.client("logs", region_name=region)

	log_group_name = "/ecs-on-demand/{}".format(event_name)
	try:
		response = logs.create_log_group(
			logGroupName=log_group_name,
		)

	except botocore.exceptions.ClientError as exception:
		if exception.response["Error"]["Code"] != 'ResourceAlreadyExistsException':
			raise exception

	task_def = {
		"family": event_name,
		"containerDefinitions": [
			{
				"name": "runner",
				"image": event["image"],
				"memoryReservation": 512,
				"essential": True,
				"logConfiguration": {
					"logDriver": "awslogs",
					"options": {
						"awslogs-group": log_group_name,
						"awslogs-region": region,
						"awslogs-stream-prefix": "runner"
					}
				}
			}
		]
	}

	if debug:
		print(task_def)

	if event.get("task_role_arn"):
		task_def["taskRoleArn"] = event["task_role_arn"]

	if event.get("privileged"):
		task_def["containerDefinitions"][0]["privileged"] = event["privileged"]

	ecs = boto3.client("ecs", region_name=region)
	ecs.register_task_definition(**task_def)

	task = {

		"cluster": event["cluster"],
		"taskDefinition": event_name,
		"overrides": {
			"containerOverrides": [
				{
					"name": "runner",
					"environment": [
						{
							"name": "DATA",
							"value": event.get("data", "")
						}
					]
				}
			]
		},
		"count": event.get("count", 1),
		"startedBy": "ecs on demand"
	}
	if event.get("environment"):
		for key, value in event.get("environment").items():
			task["overrides"]["containerOverrides"][0]["environment"].append({
				"name": key,
				"value": value,
			})

	# If throughout is set, this checks to see if the task is already running and at what scale.
	# It will only start a maximum of throughput
	if event.get("throughput"):
		tasks = ecs.list_tasks(cluster=event["cluster"], family=event_name)
		running_tasks = len(tasks["taskArns"])
		if running_tasks >= event["throughput"]:
			raise Exception("cannot start task. There are {} tasks running and the requested throughput is {}".format(running_tasks, event["throughput"]))

	fire_task = ecs.run_task(**task)

	if debug:
		print(fire_task)

	return fire_task

if __name__ == "__main__":

	event = {}
	try:
		event = {
			"image": sys.argv[1],
			"cluster": sys.argv[2],
			"throughput": 1,
			# "role": "",
		}
	except:
		print("Usage: python ecs_ondemand.py <image> <cluster> [data] [role]")
		sys.exit(1)

	run(event)
