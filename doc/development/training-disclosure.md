# Training Disclosure for collect_material_ids
This Training Disclosure, which may be more specifically titled above here (and in this document possibly referred to as "this disclosure"), is based on **Training Disclosure version 1.1.4** at https://github.com/Hierosoft/training-disclosure by Jake Gustafson. Jake Gustafson is probably *not* an author of the project unless listed as a project author, nor necessarily the disclosure editor(s) of this copy of the disclosure unless this copy is the original which among other places I, Jake Gustafson, state IANAL. The original disclosure is released under the [CC0](https://creativecommons.org/public-domain/cc0/) license, but regarding any text that differs from the original:

This disclosure also functions as a claim of copyright to the scope described in the paragraph below since potentially in some jurisdictions output not of direct human origin, by certain means of generation at least, may not be copyrightable (again, IANAL):

Various author(s) may make claims of authorship to content in the project not mentioned in this disclosure, which this disclosure by way of omission unless stated elsewhere implies is of direct human origin unless stated elsewhere. Such statements elsewhere are present and complete if applicable to the best of the disclosure editor(s) ability. Additionally, the project author(s) hereby claim copyright and claim direct human origin to any and all content in the subsections of this disclosure itself, where scope is defined to the best of the ability of the disclosure editor(s), including the subsection names themselves, unless where stated, and unless implied such as by context, being copyrighted or trademarked elsewhere, or other means of statement or implication according to law in applicable jurisdiction(s).

Disclosure editor(s): Hierosoft LLC

Project author: Hierosoft LLC

This disclosure is a voluntary of how and where content in or used by this project was produced by LLM(s) or any tools that are "trained" in any way.

The main section of this disclosure lists such tools. For each, the version, install location, and a scope of their training sources in a way that is specific as possible.

Subsections of this disclosure contain prompts used to generate content, in a way that is complete to the best ability of the disclosure editor(s).

tool(s) used:
- GPT-4-Turbo (Version 4o, chatgpt.com)

Scope of use: code described in subsections--typically modified by hand to improve logic, variable naming, integration, etc, but in this commit, unmodified.

## __init__.py

Create a blender addon that opens a configurable ids_path and saves the parsed data to known_mat_ids if the file exists, otherwise sets the variable to {}. Then iterate through all objects in the scene and when "body" in name lower(), call a function called "collect_mat_ids" with the object as the argument. The function should ensure the object is in object mode then set cache_key = os.path.splitext(os.path.split(filename)[1])[0] then known_mat_ids[cache_key] to {}. Then iterate all materials on the object in order keeping an index starting at 0, then set known_mat_ids[cache_key][material_name] = index. When done iteration, dump known_mat_ids as json to the file. Make this an add-on that can be invoked in the 3D view using a "Collect Material IDs" button. The add-on also should have a text field that is used for ids_path, with a default of ~/mat_ids.json and use expanduser to get the real path.

Pretty good but I want to use the currently open blend file path as the filename for constructing the cache key.

In addition to the mat_id_path text field, add an obj_name_filter field. Instead of the hard-coded "body" use the new settings value.

Before obj loop, set error = None and found = False. In the obj loop, set a found = True. If an object is found and found is already True, set error = "More than one object matches". After the loop if found is still False, set error = "object with {} in name not found". If error is not None, show it in the report instead of the success message.

