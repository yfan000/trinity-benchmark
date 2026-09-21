# llama-3.1-8b — vllm@frontier, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 0/2, usability 0/2, fatal; 5 of 9 requirements violated).

````
### `prompts.txt`

```python
Hello, my name is
The president of the United States is
The capital of France is
The future of AI is
I am a large language model
The climate crisis is
The benefits of renewable energy are
The importance of sustainable practices is
The impact of social media on society is
The role of artificial intelligence in healthcare is
The future of work and automation is
The benefits of virtual reality in education are
The impact of climate change on global food systems is
The importance of preserving biodiversity is
The role of governments in addressing climate change is
The benefits of electric vehicles are
The impact of social media on mental health is
The future of space exploration is
The importance of STEM education is
The role of technology in improving accessibility is
The benefits of plant-based diets are
The impact of climate change on global water systems is
The importance of protecting endangered species is
The role of individuals in addressing climate change is
The benefits of renewable energy sources are
The impact of social media on politics is
The future of transportation is
The importance of reducing plastic waste is
The role of technology in improving healthcare is
The benefits of sustainable agriculture are
The impact of climate change on global economies is
The importance of protecting natural habitats is
The role of governments in promoting sustainability is
The benefits of virtual reality in therapy are
The impact of social media on relationships is
The future of energy storage is
The importance of reducing energy consumption is
The role of technology in improving education is
The benefits of plant-based food systems are
The impact of climate change on global security is
The importance of preserving cultural heritage is
The role of individuals in promoting sustainability is
The benefits of electric vehicles in reducing emissions are
The impact of social media on business is
The future of sustainable infrastructure is
The importance of protecting indigenous communities is
The role of technology in improving accessibility for people with disabilities is
The benefits of renewable energy in reducing greenhouse gas emissions are
The impact of climate change on global food security is
The importance of preserving natural resources is
The role of governments in addressing social issues is
The benefits of virtual reality in improving mental health are
The impact of social media on the environment is
The future of sustainable transportation is
The importance of reducing waste is
The role of technology in improving healthcare outcomes is
The benefits of sustainable agriculture in reducing emissions are
The impact of climate change on global economies and societies is
The importance of protecting the ozone layer is
The role of individuals in promoting environmental sustainability is
The benefits of renewable energy sources in reducing energy costs are
The impact of social media on global politics is
The future of sustainable energy is
The importance of reducing carbon emissions is
The role of technology in improving education outcomes is
The benefits of plant-based diets in reducing emissions are
The impact of climate change on global health is
The importance of preserving natural beauty is
The role of governments in promoting environmental sustainability is
The benefits of electric vehicles in reducing air pollution are
The impact of social media on business and the economy is
The future of sustainable infrastructure development is
The importance of protecting the environment is
The role of technology in improving accessibility for people with disabilities is
The benefits of renewable energy sources in reducing greenhouse gas emissions are
The impact of climate change on global food systems and economies is
The importance of preserving natural resources and biodiversity is
The role of individuals in promoting environmental sustainability is
The benefits of virtual reality in therapy and education are
The impact of social media on the environment and global politics is
The future of sustainable transportation and energy is
The importance of reducing waste and pollution is
The role of technology in improving healthcare and education outcomes is
The benefits of sustainable agriculture and renewable energy sources are
The impact of climate change on global economies and societies is
The importance of protecting the ozone layer and natural beauty is
The role of individuals in promoting environmental sustainability and social justice is
The benefits of electric vehicles and renewable energy sources are
The impact of social media on business, the economy, and global politics is
The future of sustainable infrastructure development and energy is
The importance of protecting the environment and promoting sustainability is
The role of technology in improving accessibility and education outcomes is
The benefits of plant-based diets and renewable energy sources are
The impact of climate change on global health and economies is
The importance of preserving natural resources and biodiversity is
The role of governments in promoting environmental sustainability and social justice is
The benefits of virtual reality in therapy and education are
The impact of social media on the environment, global politics, and business is
The future of sustainable transportation and energy is
The importance of reducing waste and pollution is
The role of technology in improving healthcare and education outcomes is
The benefits of sustainable agriculture and renewable energy sources are
The impact of climate change on global economies and societies is
The importance of protecting the ozone layer and natural beauty is
The role of individuals in promoting environmental sustainability and social justice is
```

Needed: This file contains the 50 prompt strings required for the inference workload.

### `sampling_params.json`

```json
{
  "temperature": 0.8,
  "top_p": 0.95
}
```

Needed: This file contains the sampling parameters for the inference workload, including the temperature and top-p values.

### `config.json`

```json
{
  "model_path": "/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
  "batch_size": 1,
  "tensor_parallel_size": 4,
  "max_tokens": 50,
  "num_prompts": 50
}
```

Needed: This file contains the configuration parameters for the inference workload, including the model path, batch size, tensor parallel size, maximum tokens, and number of prompts.

### `model_config.json`

```json
{
  "model_name": "facebook/llama-3.1-8b",
  "tokenizer_name": "facebook/llama-3.1-8b"
}
```

Needed: This file contains the model configuration parameters, including the model name and tokenizer name.

### `inference_config.json`

```json
{
  "inference_mode": "offline",
  "num_turns": 50
}
```

Needed: This file contains the inference configuration parameters, including the inference mode and number of turns.

### `vllm_config.json`

```json
{
  "rocms_config": {
    "rocms_dir": "/usr/rocm"
  }
}
```

Needed: This file contains the vLLM configuration parameters, including the ROCm configuration.

### `vllm_runtime_config.json`

```json
{
  "runtime_config": {
    "num_gpus": 4,
    "num_gpus_per_node": 4
  }
}
```

Needed: This file contains the vLLM runtime configuration parameters, including the number of GPUs and GPUs per node.
````
