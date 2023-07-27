rule secret_code_rule
{
    strings:
        $my_text_string = "12345"

    condition:
        $my_text_string
}
