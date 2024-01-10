English | [Simplified Chinese](./README.md)
# Projects
> Yin-Yang Master Monitor Script 
# Version
> V1.0.2


# Structure
> - [static](./static/) - static files
> - [static/images](./static/images/) - images for template matching
> - [grabscreen.py](./grabscreen.py) - windows window content capture
> - [loadModel.py](./loadModel.py) - Target image loading for template matching with keyboard/mouse analog inputs
> - [test.py](./test.py) - test script


# Update log
## Activity brush for 1800 bodies
> ### New
> - [test.py](./test.py#L307-L364) added script for new event copy 1800 bodies, details:
> Recognize the lineup lock icon in the event interface, click to lock if not locked, look for the [Challenge] button to click to start the fight after locking the lineup, and loop the first step after the fight is over. (The specific process can be changed by yourself)

## V1.0.2 - January 9, 2024
> ### New
> - Class [TargetImage](./loadModel.py#L52) added [match_all](./loadModel.py#L83-L104) method to return all the targets that were matched
> - [loadModel.py](./loadModel.py) added [click](./loadModel.py#L425-L454) method, click on the specified coordinates.
> - [test.py](./test.py#L309-L329) adds a hint for the current scene in the top right corner of the hook window
> - [test.py](./test.py#L182-L306) Added handling of boundary breakthroughs, automatically go from courtyard to squatter breakthrough screen, click on the next person who fails the breakthrough
> ### Modify
> - Class [TargetImage](./loadModel.py#L52) of class [click](./loadModel.py#L106-L133) methods add random offsets of position and time to counter automated detection
> ### Fixes
> - Added [map_to_original](./loadModel.py#L29) method to fix an issue where the resolution of the monitor window and the original window did not match, resulting in inaccurate click positions.


## V1.0.1 - January 8, 2024
> ### New
> - [Check script run permissions](./test.py#L205-L208)
> - [Added simulation of keyboard/mouse input](./loadModel.py#L114-L318)
> - Class [TargetImage](./loadModel.py#L28-L70) add [click](./loadModel.py#L59-L70) methods