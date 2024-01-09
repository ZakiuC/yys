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
## V1.0.1 - January 8, 2024
### New
- [Check script run permissions](./test.py#L205-L208)
- [Added keyboard/mouse input simulation](./loadModel.py#L114-L318)
- Class [TargetImage](./loadModel.py#L28-L70) added [click](./loadModel.py#L59-L70) method

## V1.0.2 - January 9, 2024
### New
- Class [TargetImage](./loadModel.py#L52) New [match_all](./loadModel.py#L83-L104) method, which returns all the matched targets
- [loadModel.py](./loadModel.py) new [click](./loadModel.py#L425-L454) method, which clicks on the specified coordinates.
- [test.py](./test.py#L309-L329) new hint for current scene in top right corner of hook window
- [test.py](./test.py#L182-L306) added handling of boundary breakthrough, from courtyard to squatter breakthrough interface automatically, click on the next person whose breakthrough fails.
### Modify
- Class [TargetImage](./loadModel.py#L52) of class [Click](./loadModel.py#L106-L133) method to add random offsets for position and time to counteract automated detection
### Fixes
- Added [map_to_original](./loadModel.py#L29) method to fix an issue where the resolution of the monitor window and the original window did not match, resulting in inaccurate click positions.