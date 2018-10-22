<?php

namespace Tests

use Closure

/**
 * This is test file for the automatic line endings
 */
class ClassName extends AnotherClass
{
    public $var = 'test'
    CONST 'column' = 'updated_at'

    /**
     * Constructor
     * @param Closure $argument
     */
    function __construct(Closure $argument)
    {
        $variable = 'text"'

        $array = [
            'key' => 'value'
            'key' => $value
            $key  => $value

            'sub_array' => array_flatten([
                'key' => 'value'
            ])
        ]

        // PHP 7+ code
        $util->setLogger(new class {
            public function log($msg)
            {
                echo $msg;
            }
        });
    }
}