MODULE_REQUIRED_PARAMETERS = {'name'}
MODULE_OPTIONAL_PARAMETERS = {'unlock_at', 'position', 'require_sequential_progress', 'prerequisite_modules_ids', 'publish_final_grade', 'published'}

MODULE_ITEM_REQUIRED_PARAMETERS = {'type', 'content_id'}
MODULE_ITEM_OPTIONAL_PARAMETERS = {'title', 'position', 'indent', 'page_url', 'external_url', 'new_tab', 'completion_requirement', 'iframe'}

ASSIGNMENT_GROUP_REQUIRED_PARAMETERS = {}
ASSIGNMENT_GROUP_OPTIONAL_PARAMETERS = {'name', 'position', 'group_weight', 'sis_source_id', 'integration_data'}

ASSIGNMENT_REQUIRED_PARAMETERS = {'name'}
ASSIGNMENT_OPTIONAL_PARAMETERS = {'position', 'submission_types', 'allowed_extensions', 'turnitin_enabled', 'vericite_enabled', 'turnitin_settings',
    'integration_data', 'integration_id', 'peer_reviews', 'automatic_peer_reviews', 'notify_of_update', 'group_category_id', 'grade_group_students_individually',
    'external_tool_attributes', 'points_possible', 'grading_type', 'due_at', 'lock_at', 'unlock_at', 'description', 'assignment_group_id', 'assignment_overrides',
    'only_visible_to_overrides', 'published', 'grading_standard_id', 'omit_from_final_grade', 'quiz_lti', 'moderated_grading', 'grader_count', 'final_grader_id',
    'grader_comments_visible_to_graders', 'graders_anonymous_to_graders', 'graders_names_visible_to_final_grader', 'anonymous_grading', 'allowed_attempts',
    'annotatable_attachment_id'}

DISCUSSION_TOPIC_REQUIRED_PARAMETERS = {}
DISCUSSION_TOPIC_OPTIONAL_PARAMETERS = {'title', 'message', 'discussion_type', 'published', 'delayed_post_at', 'allow_rating', 'lock_at', 'podcast_enabled',
    'podcast_has_student_posts', 'require_inital_post', 'assignment', 'is_announcement', 'pinned', 'position_after', 'group_category_id', 'only_graders_can_rate',
    'sort_by_rating', 'attachment', 'specific_sections'}

PAGE_REQUIRED_PARAMETERS = {'title'}
PAGE_OPTIONAL_PARAMETERS = {'body', 'editing_roles', 'notify_of_update', 'published', 'front_page', 'publish_at'}

TEMPORARY_IDENTIFICATION_PARAMETERS = {'temp_id'}