package com.uct.smartfactory.service;

import com.uct.smartfactory.model.Asset;
import com.uct.smartfactory.repository.AssetRepository;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;

@Service
public class AssetService {

    private final AssetRepository assetRepository;

    @Autowired
    public AssetService(AssetRepository assetRepository) {
        this.assetRepository = assetRepository;
    }

    public List<Asset> getAllAssets() {
        return assetRepository.findAll();
    }

    public Asset getAssetById(Long id) {
        return assetRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Asset not found with id: " + id));
    }

    public Asset createAsset(Asset asset) {
        return assetRepository.save(asset);
    }

    public Asset updateAssetStatus(Long id, String newStatus) {
        Asset asset = assetRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Asset not found with id: " + id));
        asset.setStatus(newStatus);
        return assetRepository.save(asset);
    }

    public void deleteAsset(Long id) {
        if (!assetRepository.existsById(id)) {
            throw new RuntimeException("Asset not found with id: " + id);
        }
        assetRepository.deleteById(id);
    }

    @PostConstruct
    public void simulateInitialData() {
        if (assetRepository.count() == 0) {
            List<Asset> initialAssets = Arrays.asList(
                    new Asset(null, "CNC Lathe Machine", "RUNNING", 98.5),
                    new Asset(null, "Hydraulic Press", "MAINTENANCE", 85.0),
                    new Asset(null, "Conveyor Belt A", "RUNNING", 99.1),
                    new Asset(null, "Robotic Welding Arm", "OFFLINE", 72.4),
                    new Asset(null, "Packaging Machine", "RUNNING", 95.8)
            );
            assetRepository.saveAll(initialAssets);
        }
    }
}
