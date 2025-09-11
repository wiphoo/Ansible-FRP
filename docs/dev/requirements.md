# Ansible Requirements Management

This project uses a layered approach for managing Ansible collection dependencies to separate core role requirements from testing-specific dependencies.

## Structure

```
├── requirements.yml                              # Core collection requirements
├── roles/frp_install/
│   ├── requirements.yml                         # Role-specific requirements
│   ├── meta/main.yml                           # Role metadata with dependencies
│   └── molecule/
│       └── requirements.yml                    # Molecule testing requirements
└── galaxy.yml                                  # Collection metadata with dependencies
```

## Dependency Layers

### 1. **Core Collection Requirements** (`requirements.yml`)
- **Purpose**: Minimum collections needed to use the wiphoo.frp collection
- **Used by**: End users installing the collection
- **Contains**:
  - `community.general`: Basic system management
  - `ansible.posix`: POSIX system operations

### 2. **Role Requirements** (`roles/frp_install/requirements.yml`)
- **Purpose**: Collections specifically needed by the frp_install role
- **Used by**: Role execution
- **Contains**: Same as core requirements (role uses collection dependencies)

### 3. **Molecule Requirements** (`roles/frp_install/molecule/requirements.yml`)
- **Purpose**: Additional collections needed for testing scenarios
- **Used by**: Molecule testing framework
- **Contains**:
  - Core requirements +
  - `community.docker`: Docker container management for testing
  - `wiphoo.frp`: Collection being tested (from build artifact)

### 4. **Galaxy Dependencies** (`galaxy.yml`)
- **Purpose**: Formal collection dependencies for Ansible Galaxy
- **Used by**: Ansible Galaxy installation process
- **Contains**: Production runtime dependencies only

## Installation Commands

### For end users:
```bash
# Install collection with dependencies
ansible-galaxy collection install wiphoo.frp

# Or manually install dependencies
ansible-galaxy collection install -r requirements.yml
```

### For developers:
```bash
# Install core dependencies
ansible-galaxy collection install -r requirements.yml

# Install testing dependencies
ansible-galaxy collection install -r roles/frp_install/molecule/requirements.yml
```

### For CI/CD:
```bash
# Install core dependencies first
ansible-galaxy collection install -r requirements.yml --force -p ${{ github.workspace }}/collections

# Then install testing dependencies
ansible-galaxy collection install -r roles/frp_install/molecule/requirements.yml --force -p ${{ github.workspace }}/collections
```

## Benefits

1. **Separation of Concerns**: Core vs testing dependencies are clearly separated
2. **Minimal Production Footprint**: End users only get essential collections
3. **Comprehensive Testing**: Testing environment has all needed collections
4. **Maintainability**: Easy to update specific dependency sets
5. **CI/CD Optimization**: Different workflows can install appropriate dependencies

## Dependency Matrix

| Collection | Core | Role | Molecule | Galaxy |
|-----------|------|------|----------|---------|
| community.general | ✅ | ✅ | ✅ | ✅ |
| ansible.posix | ✅ | ✅ | ✅ | ✅ |
| community.docker | ❌ | ❌ | ✅ | ❌ |
| wiphoo.frp | ❌ | ❌ | ✅ | ❌ |

## Maintenance

When adding new dependencies:

1. **Role functionality**: Add to `galaxy.yml` and `requirements.yml`
2. **Testing only**: Add to `roles/frp_install/molecule/requirements.yml`
3. **Both**: Add to all relevant files

Keep dependencies minimal and document the reason for each requirement.
