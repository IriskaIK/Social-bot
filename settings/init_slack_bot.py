start_message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
help_message = 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?'
interests = {'Sport':['football', 'basketball','tennis'],
              'Cinema':['horror', 'drama', 'comedy']}
static_message_type = [
		{
			"type": "input",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Оберіть захоплення"
				},
				"options": [],
				"action_id": "type_select"
			},
			"label": {
				"type": "plain_text",
				"text": "Оберіть з запропонованого списку"
			}
		},
		{
			"dispatch_action": True,
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "add_own_type"
			},
			"label": {
				"type": "plain_text",
				"text": "Або додайте щось своє"
			}
		}
	]
static_empty_message_category = [
		{
			"dispatch_action": True,
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "add_own_category"
			},
			"label": {
				"type": "plain_text",
				"text": "Додати щось своє"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Або можете залишити обране "
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Click Me"
				},
				"value": "click_me_123",
				"action_id": "choose_current_type"
			}
		}
	]
static_message_category = [
		{
			"type": "input",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Оберіть захоплення"
				},
				"options": [],
				"action_id": "category_select"
			},
			"label": {
				"type": "plain_text",
				"text": "Оберіть з запропонованого списку"
			}
		},
		{
			"dispatch_action": True,
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "add_own_category"
			},
			"label": {
				"type": "plain_text",
				"text": "Або додайте щось своє"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Або можете залишити обране "
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Click Me"
				},
				"value": "click_me_123",
				"action_id": "choose_current_type"
			}
		}
	]

static_option = {
						"text": {
							"type": "plain_text",
							"text": ""
						},
						"value": ""
					}
direct_mess_help = [
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Додати захоплення"
					},
					"style": "primary",
					"value": "button_add_type",
					"action_id": "button_add_type"
				}
			]
		}
	]

direct_mess_start = [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Привіт, додай свої інтереси, обераючи серед запропанованих, або написавши свої"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Додати захоплення"
					},
					"style": "primary",
					"value": "button_add_type",
					"action_id": "button_add_type"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Допомога"
					},
					"style": "danger",
					"value": "button_help",
					"action_id": "button_help"
				}
			]
		}
	]

slack_app_token = 'xapp-1-A02PQEA02D6-2779837001541-79031d37e278e7a391b23e8ad0d6cb972c055c4e6bd16ff00a4924d9caf2829b'
signing_secret = '195e6342a19a9d4505f85c8cef7c6ca4'