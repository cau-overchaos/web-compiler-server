use std::collections::HashMap;
use std::vec::Vec;

use crate::{
    executor::{execute, ExecuteOption, ResourceLimit},
    process::Directory,
};

pub struct CompileOption {
    pub language: String,
    pub input_path: String,
    pub output_path: String,
    pub time_limit: u64,
}

pub struct RunOption {
    pub language: String,
    pub file_path: String,
    pub input_path: Option<String>,
    pub output_path: Option<String>,
    pub answer_path: Option<String>,
    pub time_limit: u64,
    pub memory_limit: u64,
    pub envs: Vec<String>,
    pub directory: Directory,
}

enum FlagToken {
    INPUT,
    OUTPUT,
    BINARY,
}

impl FlagToken {
    fn value(&self) -> &str {
        match *self {
            FlagToken::INPUT => "<INPUT>",
            FlagToken::OUTPUT => "<OUTPUT>",
            FlagToken::BINARY => "<BINARY>",
        }
    }
}

fn get_compile_flags(language: &str) -> Option<(&str, Vec<&str>)> {
    let map: HashMap<&str, (&str, Vec<&str>)> = [
        (
            "c",
            (
                "/usr/bin/gcc",
                vec![
                    "gcc",
                    FlagToken::INPUT.value(),
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
        (
            "c99",
            (
                "/usr/bin/gcc",
                vec![
                    "gcc",
                    FlagToken::INPUT.value(),
                    "-std=gnu99",
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
        (
            "c11",
            (
                "/usr/bin/gcc",
                vec![
                    "gcc",
                    FlagToken::INPUT.value(),
                    "-std=gnu11",
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
        (
            "c17",
            (
                "/usr/bin/gcc",
                vec![
                    "gcc",
                    FlagToken::INPUT.value(),
                    "-std=gnu17",
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
        (
            "cpp",
            (
                "/usr/bin/g++",
                vec![
                    "g++",
                    FlagToken::INPUT.value(),
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
        (
            "cpp98",
            (
                "/usr/bin/g++",
                vec![
                    "g++",
                    FlagToken::INPUT.value(),
                    "-std=gnu++98",
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
        (
            "cpp11",
            (
                "/usr/bin/g++",
                vec![
                    "g++",
                    FlagToken::INPUT.value(),
                    "-std=gnu++11",
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
        (
            "cpp14",
            (
                "/usr/bin/g++",
                vec![
                    "g++",
                    FlagToken::INPUT.value(),
                    "-std=gnu++14",
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
        (
            "cpp17",
            (
                "/usr/bin/g++",
                vec![
                    "g++",
                    FlagToken::INPUT.value(),
                    "-std=gnu++17",
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
        (
            "cpp20",
            (
                "/usr/bin/g++",
                vec![
                    "g++",
                    FlagToken::INPUT.value(),
                    "-std=gnu++20",
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
        (
            "cpp2a",
            (
                "/usr/bin/g++",
                vec![
                    "g++",
                    FlagToken::INPUT.value(),
                    "-std=gnu++2a",
                    "-O2",
                    "-Wall",
                    "-lm",
                    "-o",
                    FlagToken::OUTPUT.value(),
                    "-DONLINE_JUDGE",
                    "-DBOJ",
                ],
            ),
        ),
    ]
    .iter()
    .cloned()
    .collect();

    map.get(language).cloned()
}

fn get_run_flags(language: &str) -> Option<Vec<&str>> {
    let map: HashMap<&str, Vec<&str>> = [
        ("c", vec![FlagToken::BINARY.value()]),
        ("cpp", vec![FlagToken::BINARY.value()]),
        ("python", vec![FlagToken::BINARY.value()]),
    ]
    .iter()
    .cloned()
    .collect();

    map.get(language).cloned()
}

pub fn compile(opt: CompileOption) -> i32 {
    let compiler: &str;
    let compile_args: Vec<&str>;
    match get_compile_flags(&opt.language) {
        Some(flags) => {
            compiler = flags.0;
            compile_args = flags.1;
        }
        _ => {
            panic!("unsupported language: {}", opt.language);
        }
    }

    let compile_args: Vec<&str> = compile_args
        .iter()
        .map(|arg| {
            if *arg == FlagToken::INPUT.value() {
                return opt.input_path.as_str();
            } else if *arg == FlagToken::OUTPUT.value() {
                return opt.output_path.as_str();
            }

            *arg
        })
        .collect();

    execute(
        compiler,
        compile_args,
        ExecuteOption {
            envs: None,
            limits: Some(ResourceLimit {
                time: opt.time_limit,
                memory: 536870912, // 512mb
            }),
            input_path: None,
            output_path: None,
            answer_path: None,
            directory: None,
            use_syscall: false,
        },
    )
}

pub fn run(opt: RunOption) -> i32 {
    let args = match get_run_flags(&opt.language) {
        Some(args) => args,
        None => {
            panic!("unsupported language: {}", opt.language);
        }
    };

    let args: Vec<&str> = args
        .iter()
        .map(|arg| {
            if *arg == FlagToken::BINARY.value() {
                return opt.file_path.as_str();
            }

            *arg
        })
        .collect();

    println!("{:?}", args);
    let rlimit = ResourceLimit {
        time: opt.time_limit,
        memory: opt.memory_limit,
    };

    let option = ExecuteOption {
        envs: Some(opt.envs.clone()),
        limits: Some(rlimit),
        input_path: opt.input_path.clone(),
        output_path: opt.output_path.clone(),
        answer_path: opt.answer_path.clone(),
        directory: Some(opt.directory.clone()),
        use_syscall: true,
    };

    execute(&opt.file_path, args, option)
}
