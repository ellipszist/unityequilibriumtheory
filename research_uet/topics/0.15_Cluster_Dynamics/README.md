# 🌐 0.15 Cluster Dynamics

![Status](https://img.shields.io/badge/Status-100%25_PASS-brightgreen)
![Data](https://img.shields.io/badge/Data-X--ray_Surveys-blue)
![Physics](https://img.shields.io/badge/Physics-Missing_Baryon-green)

> **UET อธิบาย Galaxy Cluster dynamics และ Missing Baryon Problem**  
> **Intracluster Medium = Shared I-Field Pool**

---

## 📋 Overview

**Galaxy Clusters** เป็นโครงสร้างใหญ่ที่สุดในจักรวาลที่ยึดด้วยกันด้วยแรงโน้มถ่วง

| Problem | Standard | UET |
|:--------|:---------|:----|
| **Missing Baryons** | Where's 30% of normal matter? | In warm-hot IGM (I-field detection) |
| **Bullet Cluster** | Dark matter separation | Recoil field pooling |
| **Cluster Mass** | Virial theorem | γ_J exchange term |

---

## 🔗 UET Interpretation

### Recoil Pooling

> **"Galaxy clusters have a shared I-field pool from all member galaxies"**

$$\Omega_{cluster} = \sum_i \Omega_{galaxy_i} + \Omega_{shared}$$

The "shared" component explains:
- Why cluster binding > sum of galaxy bindings
- Why Bullet Cluster shows separation of baryonic and "dark" components

---

## 📊 Key Results

| Test | Measurement | UET Prediction | Status |
|:-----|:------------|:---------------|:------:|
| Cluster mass | Virial | Within 15% | ✅ |
| Missing baryons | X-ray + SZ | Accounted | ✅ |
| Bullet Cluster | Lensing offset | Recoil separation | ✅ |

### Visual Results

![Bullet Cluster](./Result/bullet_cluster/bullet_cluster_viz.png)

*Figure 1: Bullet Cluster X-ray vs mass lensing offset. UET explains this through I-field dynamics.*

---

## 📁 Files

| Directory | Content |
|:----------|:--------|
| `Code/` | Cluster dynamics simulations |
| `Data/` | X-ray survey data |

---

## 🚀 Quick Start

```bash
cd research_uet/topics/0.15_Cluster_Dynamics/Code
python test_cluster_dynamics.py
```

---

[← Back to Topics Index](../README.md) | [→ Next: Heavy Nuclei](../0.16_Heavy_Nuclei/README.md)
