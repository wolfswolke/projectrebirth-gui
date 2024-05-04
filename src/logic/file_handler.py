# Patching instructions would look like this:
# steam = {"app_id": 480,
# "depot_id": 481,
# "manifest_id": 3183503801510301321
# }
# .\bnetinstaller.exe --prod prot --uid prometheus_test --lang enus --dir "<PATH>"
# battlenet = {
# "product": "prot",
# "uid": "prometheus_test",
# "lang": "enus"
# }
#         provider = "steam"
#         provider_value = steam
#         return jsonify({
#             "instructions": {
#                 "delete": [
#                     "path/file1",
#                     "path/sub/file2"
#                 ],
#                 "move": [
#                     {
#                         "name": "file1",
#                         "source": "path/sub/",
#                         "location": "path/sub2"
#                     }
#                 ],
#                 "download": [
#                     {
#                         "name": "game.exe",
#                         "location": "path/sub3"
#                     }
#                 ]
#             },
#             "files": [
#                 {
#                     "name": "game.exe",
#                     "id": "1238712381283"
#                 },
#                 {
#                     "name": "patch.dll",
#                     "id": "184563454568"
#                 }
#             ],
#             "provider": provider,
#             provider: provider_value
#         })
